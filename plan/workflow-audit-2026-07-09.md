# Research Workflow Audit - 2026-07-09

## 1. Audit Scope

This audit covers the active research workflow under `plan/`, the Optical-SAR pivot, Arbor state,
MoA/reviewer contracts, experiment governance, monitor ownership, and security-sensitive runtime
practices.

The audit is a snapshot, not an implementation record. No issue below should be considered fixed
until the corresponding acceptance condition is verified from files and artifacts.

## 2. Executive Verdict

The research direction is now substantially clearer: Optical-SAR open-vocabulary segmentation is the
primary substrate, with selective prediction and failure-source attribution as the method target.
The high-level venue framing is compatible with Information Fusion / ESWA.

However, the workflow is **not launch-ready for an autonomous `/goal` loop**. The main blockers are:

1. Arbor still points to the archived `aerial-vln` run.
2. The MM-OVSeg reproduce-first contract does not yet name an exact model, checkpoint, split, command,
   paper target, tolerance, `B_dev`, and sealed `B_test`.
3. The documented loop orders `/forge` before the baseline run, conflicting with reproduce-first.
4. Active indexes and scouting documents still route agents toward deleted or archived directions.
5. Evaluation metrics, attribution labels, statistical units, and reviewer independence are not defined
   tightly enough to prevent flexible post-hoc interpretation.

Recommendation: perform a bounded workflow refactor before starting the autonomous research loop.

## 3. Findings by Severity

### P0 - Must Fix Before Launch

#### P0.1 Stale Arbor Active Run

- Evidence: `.arbor/active-run` contains `aerial-vln`.
- Evidence: no canonical Optical-SAR Arbor session is active.
- Risk: new nodes, scores, reports, and resume events can be attached to the previous VLA campaign.
- Required fix: initialize an `optical-sar` Arbor session, set its launch metadata, and switch
  `.arbor/active-run` only after validating the session directory.
- Acceptance: `tree_view` and generated reports resolve exclusively to the Optical-SAR session.

#### P0.2 Incomplete Reproduction Contract

- Evidence: `plan/optical-sar-research-plan.md` names MM-OVSeg but does not lock the exact B16/L14
  variant, checkpoint, configuration, evaluation command, paper table cell, tolerance, and split.
- Evidence: the local repository has packaged source archives that still require validation/extraction;
  official processed data/checkpoint availability is dynamic.
- Risk: a run may be called a reproduction while silently changing backbone, preprocessing, split, or
  metric implementation.
- Required fix: create a machine-checkable launch contract containing:
  - repository commit and environment lock;
  - model variant and checkpoint hash;
  - dataset version, setting, and split;
  - exact evaluation command;
  - original paper table/row/column and target value;
  - allowed tolerance and failure action;
  - named `B_dev` and sealed `B_test`.
- Acceptance: a clean shell can execute the command and produce a parsed metric artifact without manual
  source edits.

#### P0.3 Reproduce-First Ordering Conflict

- Evidence: `plan/goal-directive.md` requires reproduction before `/forge`.
- Evidence: the standard loop is documented as `/prospect -> /forge -> /prereg -> run`.
- Risk: agents can either violate reproduce-first or run an unregistered baseline without preregistration.
- Required fix: define two explicit phases:
  1. `INIT -> baseline preregistration -> reproduce -> exp-verify`.
  2. `prospect -> forge -> method preregistration -> run -> exp-verify -> adversary -> autopsy`.
- Acceptance: there is one unambiguous state transition diagram and one authoritative loop definition.

#### P0.4 Runtime Credential Exposure

- Observation during audit: an active download command exposed an `HF_TOKEN` value in its process
  command line. The value is intentionally omitted here.
- Risk: credentials can be read through process inspection, shell history, monitoring, or logs.
- Required fix: pass secrets through a protected environment file, inherited environment, credential
  cache, or wrapper that does not include literal secrets in argv. Rotate the affected token if the host
  is shared or process visibility is not private.
- Acceptance: `ps` and download logs contain no token values; `.env` permissions are restricted.

### P1 - Fix Before Claim-Bearing Experiments

#### P1.1 Evaluation Protocol Is Under-Specified

- Current metrics include mIoU, seen/unseen mIoU, AURC, selective mIoU/ECE, accepted-set mIoU, and
  attribution quality, but their exact definitions are absent.
- Missing decisions include risk definition, coverage grid, binning, averaging, ignored pixels, class
  weighting, scene/image aggregation, and confidence tie handling.
- Required fix: add one canonical Optical-SAR evaluation protocol with formulas and executable metric
  entrypoints.
- Statistical unit must be image/scene or dataset unit, not independent pixels.
- Learned methods require seed reporting; deterministic checkpoint reproduction does not need fake seeds.
- Prefer paired image/scene bootstrap or hierarchical bootstrap over pixel-level significance tests.

#### P1.2 Failure-Source Labels and Anti-Shortcut Controls Are Undefined

- The target concepts are semantic novelty, sensor corruption, cross-modal conflict, and optionally
  misregistration.
- The current documents do not define how each label is constructed without using information unavailable
  at inference time or leaking the evaluation intervention.
- `instruction-free labels` in `plan/goal-directive.md` is a stale VLA term and is not meaningful here.
- Required fix: define label provenance, training visibility, held-out corruption families, severity
  splits, conflict construction, and counterfactual modality tests.

#### P1.3 Stale Active Scouting Index

- Evidence: `plan/README.md` presents `plan/scouting/README.md` as current.
- Evidence: `plan/scouting/README.md` still ranks TbV, OpenFly, C5, and references removed data paths.
- Risk: a resumed agent can legally route back to archived campaigns.
- Required fix: either rewrite the scouting index for Optical-SAR or move the old index under a dated
  archive and remove it from active navigation.

#### P1.4 Dynamic Status Is Duplicated

- Download and asset status appears in planning documents as well as runtime manifests/logs.
- Risk: static plans become false while downloads continue, causing duplicate downloads or incorrect gates.
- Required fix: keep stable requirements in plans; keep volatile availability, byte counts, hashes, and
  active process state in `openbuild/optical_sar/DATA_ASSETS.md` or a generated status file.

#### P1.5 Reviewer Independence Is Not Enforced by Provenance

- Codex/GPT can participate in MoA proposal generation and later be selected as an independent rescue or
  adversarial reviewer.
- A co-proposer cannot independently validate its own claim.
- Required fix: record per-node proposer identities and exclude them from independent grant/review roles.
  When Codex co-proposed a node, route independent review to a non-participating substrate.

### P2 - Refactor for Reliability and Maintainability

#### P2.1 Conflicting MoA Specifications

- `plan/moa-advisor-panel-design-2026-07-04.md` says all advisors receive the same packet.
- `moa/router-protocol.md` specifies differentiated lanes, frames, operators, and dropout.
- Required fix: make the differentiated router the single runtime authority; archive or rewrite the older
  same-packet specification.

#### P2.2 Monitor Ownership Is Policy-Only

- The documents correctly require the parent/main agent to own every outliving monitor.
- There is no canonical monitor registry path, schema, heartbeat, or completion handoff artifact.
- Required fix: add a main-agent monitor registry containing task ID, owner, command/session, start time,
  expected event, terminal state, and resume target. Subagent-local monitors must not satisfy the rule.

#### P2.3 Backup Promotion Authority Is Ambiguous

- The workflow says tactical questions should go to Codex and humans should only be interrupted for a
  forced domain/dataset change.
- P0 -> P1/P2 promotions are predeclared but not explicitly marked as autonomously authorized.
- Required fix: state that promotion within the approved Optical-SAR portfolio is automatic after a
  preregistered kill; human approval is required only to leave the portfolio, incur an exceptional
  resource commitment, or relax the scientific bar.

#### P2.4 Operating Manual Contains Historical Contradictions

- `plan/operating-manual.md` is large and mixes current rules with historical VLA/score-chasing language.
- Risk: agents can cite an old lower section to justify actions that contradict the current top-level state.
- Required fix: split it into a short normative manual and dated archival rationale. Normative rules should
  be unique, concise, and testable.

#### P2.5 Backup Baseline Fidelity

- M2CD is useful related work but is not currently a safe reproduce-first anchor: the repository has no
  released checkpoint and contains author-local paths.
- CMCDNet/CAU-Flood is the more stable P1 anchor until M2CD is independently made reproducible.
- Required fix: encode this distinction in the backup launch contract rather than treating both as equal.

## 4. Normative Design Problems

The current workflow has good principles but too many duplicated authorities. The refactor should enforce
the following hierarchy:

1. `goal-directive.md`: compact objective, hard constraints, portfolio, human gates.
2. `operating-manual.md`: stable workflow state machine and evidence rules.
3. Track launch contract: exact dataset/model/metric/reproduction specification.
4. Runtime manifests: downloads, processes, monitors, artifacts, and hashes.
5. Arbor state: idea tree, node status, score metadata, and merge/report history.
6. RUNLOG: chronological scientific interpretation; never the sole source of executable truth.

No rule should be defined differently in two active documents. Historical explanations belong in
`plan/archive/`, not behind a `deprecated` label inside an active manual.

## 5. Proposed Refactor Sequence

### Phase A - State Isolation

1. Create and activate the Optical-SAR Arbor session.
2. Archive stale active indexes and remove dead path references.
3. Establish one runtime asset/status manifest and one monitor registry.
4. Remove credentials from process arguments and rotate if necessary.

### Phase B - Reproduction Contract

1. Select the first MM-OVSeg model/checkpoint and exact table setting.
2. Name `B_dev` and sealed `B_test`.
3. Lock repository commit, environment, dataset hashes, command, parser, target, and tolerance.
4. Preregister and execute the baseline reproduction before method ideation.

### Phase C - Scientific Protocol

1. Define failure-source labels and anti-leak controls.
2. Define selective-prediction and calibration metrics exactly.
3. Define image/scene-level statistical analysis and seed policy.
4. Define the phenomenon gate and its automatic P0 -> P1 promotion rule.

### Phase D - Agent Governance

1. Reconcile MoA packet/router specifications.
2. Track proposer/reviewer provenance per node.
3. Enforce main-agent monitor ownership through a registry.
4. Reduce the operating manual to a single executable state machine.

## 6. Launch Acceptance Checklist

The autonomous `/goal` loop may start only when all items below are true:

- [ ] `.arbor/active-run` points to a valid Optical-SAR session.
- [ ] The baseline launch contract names model, checkpoint, hash, split, command, target, and tolerance.
- [ ] `B_dev` and sealed `B_test` are explicit and accessible.
- [ ] The official baseline command completes and emits a parsed artifact.
- [ ] Reproduce-first and method-development loops have one unambiguous order.
- [ ] Metric formulas and statistical units are fixed before inspecting method results.
- [ ] Failure-source labels and shortcut controls are documented.
- [ ] Active indexes contain no archived campaign or deleted-data routes.
- [ ] Download status and monitor state have canonical runtime manifests.
- [ ] No credentials appear in argv, logs, or tracked files.
- [ ] MoA proposer identities and independent reviewer eligibility are recorded.
- [ ] P0 -> P1/P2 promotion is explicitly authorized without a human menu.

## 7. Current Disposition

**Status: REFACTOR REQUIRED BEFORE AUTONOMOUS LAUNCH.**

The Optical-SAR direction itself is not rejected. The present risk is procedural: without state isolation,
an exact reproduction contract, and fixed evaluation semantics, the workflow can repeat the earlier pattern
of generating sophisticated mechanisms on an unverified substrate. The upgrade task should close the P0
items first, then proceed through the acceptance checklist rather than rewriting the research idea again.
