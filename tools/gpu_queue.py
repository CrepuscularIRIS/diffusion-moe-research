#!/usr/bin/env python3
"""gpu_queue.py — keep every GPU busy: schedule shell-script jobs across GPU slots.

v1 = batch runner (see plan/gpu-job-queue-plan-2026-07-10.md). Autonomous: no human
interaction; the state file + per-job logs are the source of truth; the /goal parent
polls `status` instead of blocking on the run.

Usage:
  gpu_queue.py run [--gpus 0,1] [--cap-hours 6] [--poll 5] [--logdir DIR] [--state FILE] JOB.sh [JOB.sh ...]
  gpu_queue.py status [--state FILE]

Each JOB.sh is launched as `CUDA_VISIBLE_DEVICES=<gpu> bash JOB.sh`, pinned to one GPU,
detached in its own process group, stdout+stderr -> <logdir>/<job>.<ts>.log. When a GPU
slot frees, the next queued job is pulled IMMEDIATELY (no idle-while-queued). Each job is
hard-killed at --cap-hours (SIGTERM, then SIGKILL after a grace period).
"""
import argparse, json, os, signal, subprocess, sys, time
from datetime import datetime, timezone


def _now():
    return datetime.now(timezone.utc)


def _iso(dt):
    return dt.replace(microsecond=0).isoformat()


def _write_state(path, gpus, queued, completed):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump({
            "updated": _iso(_now()),
            "gpus": gpus,
            "queued": [os.path.basename(j) for j in queued],
            "completed": completed,
        }, f, indent=2)
    os.replace(tmp, path)  # atomic


def cmd_run(a):
    gpu_ids = [g.strip() for g in a.gpus.split(",") if g.strip() != ""]
    if not gpu_ids:
        print("ERROR: no GPUs given", file=sys.stderr)
        return 2
    if len(set(gpu_ids)) != len(gpu_ids):
        gpu_ids = list(dict.fromkeys(gpu_ids))
        print(f"WARNING: duplicate GPU ids in --gpus {a.gpus}; deduped to {gpu_ids}", file=sys.stderr)
    cap_s = int(a.cap_hours * 3600)
    os.makedirs(a.logdir, exist_ok=True)
    queue = list(a.jobs)
    for j in queue:
        if not os.path.isfile(j):
            print(f"ERROR: job script not found: {j}", file=sys.stderr)
            return 2
    slots = {g: None for g in gpu_ids}  # gpu -> running dict or None
    completed = []

    def snapshot():
        gpus = {}
        for g, s in slots.items():
            if s is None:
                gpus[g] = {"state": "idle"}
            else:
                gpus[g] = {"state": "running", "job": os.path.basename(s["job"]),
                           "pid": s["proc"].pid, "start": _iso(s["start"]),
                           "elapsed_s": int((_now() - s["start"]).total_seconds()),
                           "log": s["log"]}
        _write_state(a.state, gpus, queue, completed)

    def launch(g, job):
        ts = _now().strftime("%Y%m%dT%H%M%S_%f")  # microseconds -> no same-second collision
        log = os.path.join(a.logdir, f"{os.path.basename(job)}.{ts}.log")
        env = dict(os.environ, CUDA_VISIBLE_DEVICES=g)
        lf = open(log, "w")
        try:
            lf.write(f"# gpu_queue: {job} on GPU {g} @ {_iso(_now())}\n")
            lf.flush()
            p = subprocess.Popen(["bash", job], env=env, stdout=lf,
                                 stderr=subprocess.STDOUT, start_new_session=True)
        except Exception:
            lf.close()  # no fd leak if Popen fails
            raise
        slots[g] = {"proc": p, "job": job, "start": _now(), "log": log, "lf": lf}
        print(f"[launch] GPU{g} <- {os.path.basename(job)} (pid {p.pid}) log {log}")

    def kill_pg(proc, sig):
        try:
            os.killpg(os.getpgid(proc.pid), sig)
        except ProcessLookupError:
            pass

    print(f"[gpu_queue] {len(queue)} jobs across GPUs {gpu_ids}; cap {a.cap_hours}h; state {a.state}")
    while queue or any(s is not None for s in slots.values()):
        for g in gpu_ids:                        # fill free slots
            if slots[g] is None and queue:
                launch(g, queue.pop(0))
        for g in gpu_ids:                        # poll running
            s = slots[g]
            if s is None:
                continue
            rc = s["proc"].poll()
            elapsed = (_now() - s["start"]).total_seconds()
            if rc is None and elapsed > cap_s:
                print(f"[cap] GPU{g} {os.path.basename(s['job'])} exceeded {a.cap_hours}h -> kill")
                kill_pg(s["proc"], signal.SIGTERM)
                try:
                    s["proc"].wait(timeout=30)
                except subprocess.TimeoutExpired:
                    kill_pg(s["proc"], signal.SIGKILL)
                rc = s["proc"].wait()  # blocking reap: guaranteed real exit code, clears slot
            if rc is not None:
                s["lf"].flush()
                s["lf"].close()
                dur = int((_now() - s["start"]).total_seconds())
                completed.append({"job": os.path.basename(s["job"]), "gpu": g,
                                  "exit": rc, "duration_s": dur, "log": s["log"]})
                print(f"[done] GPU{g} {os.path.basename(s['job'])} exit={rc} dur={dur}s")
                slots[g] = None
        snapshot()
        if queue or any(s is not None for s in slots.values()):
            time.sleep(a.poll)
    snapshot()
    print("\n[gpu_queue] SUMMARY")
    ok = sum(1 for c in completed if c["exit"] == 0)
    for c in completed:
        print(f"  {c['job']:32s} GPU{c['gpu']} exit={c['exit']} dur={c['duration_s']}s")
    print(f"[gpu_queue] {ok}/{len(completed)} jobs exit 0")
    return 0 if ok == len(completed) else 1


def cmd_status(a):
    if not os.path.isfile(a.state):
        print(f"no state file at {a.state}")
        return 0
    with open(a.state) as f:
        d = json.load(f)
    print(f"gpu_queue status @ {d.get('updated')}")
    for g, s in d.get("gpus", {}).items():
        if s.get("state") == "running":
            print(f"  GPU{g}: RUNNING {s['job']} ({s['elapsed_s']}s, pid {s['pid']})")
        else:
            print(f"  GPU{g}: idle")
    q = d.get("queued", [])
    print(f"  queued: {len(q)}" + (f" -> {q}" if q else ""))
    comp = d.get("completed", [])
    if comp:
        print(f"  completed: {len(comp)}")
        for c in comp[-5:]:
            print(f"    {c['job']} GPU{c['gpu']} exit={c['exit']} dur={c['duration_s']}s")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="gpu_queue.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="schedule jobs across GPUs")
    r.add_argument("--gpus", default="0,1", help="comma-separated GPU ids (default 0,1)")
    r.add_argument("--cap-hours", type=float, default=6.0, dest="cap_hours")
    r.add_argument("--poll", type=float, default=5.0, help="poll interval seconds")
    r.add_argument("--logdir", default="gpu_queue_logs")
    r.add_argument("--state", default="gpu_queue_state.json")
    r.add_argument("jobs", nargs="+", help="job shell scripts")
    r.set_defaults(func=cmd_run)
    s = sub.add_parser("status", help="print queue/GPU status")
    s.add_argument("--state", default="gpu_queue_state.json")
    s.set_defaults(func=cmd_status)
    a = ap.parse_args()
    sys.exit(a.func(a))


if __name__ == "__main__":
    main()
