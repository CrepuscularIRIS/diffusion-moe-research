对，**`/goal` 的本质就是一个“会话级 prompt-based Stop hook”**：每一轮 Claude 结束后触发一个 Stop evaluator；evaluator 看当前 conversation 里有没有满足 goal；如果没有，就返回“继续工作 + 原因”；如果满足，就放行停止。官方文档也明确说 `/goal` 是 session-scoped shortcut，而固定 Stop hook 是写在 settings 里的持久配置。([Claude Code][1])

你要做“高度自定义版 `/goal`”，最稳不是去复制内置 `/goal`，而是做这个结构：

```text
/autogoal <你的目标参数>
        ↓
自定义 skill / slash command 写入 .claude/autogoal.json
        ↓
固定 Stop hook 每轮读取 autogoal.json
        ↓
没达标：返回 {"decision":"block","reason":"下一步指令"}
达标：exit 0，允许 Claude 停止
```

这样你只需要**安装一次 Stop hook**，之后每个项目用 `/autogoal xxx` 开启不同策略。

---

## 1. `/goal` 实现机制是什么？

官方目前的描述很清楚：

```text
/goal = session-scoped prompt-based Stop hook
```

它每轮结束后，把 goal condition 和当前 conversation 发给一个小模型 evaluator，默认是 fast/small model；evaluator 返回 yes/no 和 reason。`no` 会让 Claude 继续下一轮，`yes` 会清除 goal 并记录 achieved。([Claude Code][1])

所以它的伪代码大概是：

```ts
onStop(turn) {
  if (!session.goal) return allowStop()

  const result = smallModel.evaluate({
    goal: session.goal,
    transcript: conversationSoFar
  })

  if (result.ok) {
    session.goal = null
    return allowStop()
  }

  return blockStop(result.reason)
}
```

但它有一个限制：evaluator **不会自己跑命令或读文件**，它只看 Claude 在对话里展示出来的证据。所以如果你想要“必须真的跑测试、必须检查 git diff、必须看 QUEUE 文件”，就要用 command hook 或 agent hook，而不是只用 prompt hook。([Claude Code][1])

---

## 2. 你要做的不是“动态创建 Stop hook”，而是“固定 Stop hook + 动态状态文件”

Stop hook 写在 `.claude/settings.local.json` 或 `.claude/settings.json` 里。官方支持的 hook 位置包括全局 `~/.claude/settings.json`、项目 `.claude/settings.json`、项目本地 `.claude/settings.local.json`，以及 plugin/skill/agent 等作用域。([Claude Code][2])

**重点：Stop event 不支持 matcher**。也就是说你不能写“只在 `/autogoal` 时触发的 Stop hook”；Stop hook 会每轮都触发。正确做法是让 Stop hook 每轮先检查：

```text
.claude/autogoal.json 是否存在且 active=true
```

不存在就 `exit 0`，等于无事发生。

---

## 3. 最小可用版：自定义 `/autogoal` + 固定 Stop hook

目录结构：

```text
.claude/
  settings.local.json
  skills/
    autogoal/
      SKILL.md
  hooks/
    autogoal-stop.mjs
  autogoal.json
  QUEUE.md
  RUNLOG.md
  BLOCKED.md
```

### `.claude/settings.local.json`

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node ${CLAUDE_PROJECT_DIR}/.claude/hooks/autogoal-stop.mjs",
            "timeout": 20,
            "statusMessage": "Checking AutoGoal stop condition..."
          }
        ]
      }
    ]
  }
}
```

Stop hook 可以用 top-level `decision: "block"` 阻止 Claude 停止；Claude 会把 `reason` 作为下一步反馈给模型。官方 hooks guide 也说明 `Stop` 和 `PostToolUse` 这类事件使用 top-level `decision: "block"`，而不是 `hookSpecificOutput.permissionDecision` 那套。([Claude Code][3])

---

## 4. `.claude/hooks/autogoal-stop.mjs`

这是核心。它每轮结束时检查 `.claude/autogoal.json`、`.claude/QUEUE.md`、`.claude/RUNLOG.md`。没达标就 block，让 Claude 继续。

```js
#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

function readStdin() {
  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => (data += chunk));
    process.stdin.on("end", () => resolve(data));
  });
}

function exists(p) {
  try {
    return fs.existsSync(p);
  } catch {
    return false;
  }
}

function read(p) {
  try {
    return fs.readFileSync(p, "utf8");
  } catch {
    return "";
  }
}

function mtimeAgeMinutes(p) {
  try {
    const stat = fs.statSync(p);
    return (Date.now() - stat.mtimeMs) / 60000;
  } catch {
    return Infinity;
  }
}

function block(reason) {
  process.stdout.write(JSON.stringify({ decision: "block", reason }) + "\n");
  process.exit(0);
}

async function main() {
  const inputRaw = await readStdin();
  let input = {};
  try {
    input = JSON.parse(inputRaw || "{}");
  } catch {
    process.exit(0);
  }

  const cwd = input.cwd || process.env.CLAUDE_PROJECT_DIR || process.cwd();

  const autogoalPath = path.join(cwd, ".claude", "autogoal.json");
  const queuePath = path.join(cwd, ".claude", "QUEUE.md");
  const runlogPath = path.join(cwd, ".claude", "RUNLOG.md");
  const blockedPath = path.join(cwd, ".claude", "BLOCKED.md");

  if (!exists(autogoalPath)) process.exit(0);

  let cfg = {};
  try {
    cfg = JSON.parse(read(autogoalPath));
  } catch {
    block("AutoGoal config is invalid JSON. Fix .claude/autogoal.json before stopping.");
  }

  if (!cfg.active) process.exit(0);

  // 防止 Stop hook 因自己 block 后立刻再次无限 block。
  // 官方文档建议检查 stop_hook_active；连续 block 太多会 hit block cap。
  if (input.stop_hook_active === true) {
    process.exit(0);
  }

  const maxTurns = Number(cfg.maxTurns || 20);
  const statePath = path.join(cwd, ".claude", ".autogoal-state.json");

  let state = { turns: 0 };
  if (exists(statePath)) {
    try {
      state = JSON.parse(read(statePath));
    } catch {}
  }
  state.turns = Number(state.turns || 0) + 1;
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2));

  if (state.turns > maxTurns) {
    cfg.active = false;
    fs.writeFileSync(autogoalPath, JSON.stringify(cfg, null, 2));
    block(
      `AutoGoal reached maxTurns=${maxTurns}. Stop doing new work. Summarize current state, blockers, changed files, and next recommended slice.`
    );
  }

  const queue = read(queuePath);
  const runlog = read(runlogPath);
  const blocked = read(blockedPath);

  const hasUncheckedQueue = /^[ \t]*[-*][ \t]+\[[ \t]\]/m.test(queue);
  const hasFreshRunlog = exists(runlogPath) && mtimeAgeMinutes(runlogPath) <= Number(cfg.runlogFreshMinutes || 45);
  const hasBlocked = blocked.trim().length > 0 && /blocked|阻塞|cannot|无法|需要人工|human/i.test(blocked);

  if (cfg.mode === "queue") {
    if (hasUncheckedQueue && !hasBlocked) {
      block(
        [
          "AutoGoal is still active.",
          "QUEUE.md still contains unchecked items.",
          "Continue with the first unchecked item only.",
          "Before stopping, update RUNLOG.md with:",
          "- current item",
          "- changed files",
          "- exact verification commands",
          "- exit codes",
          "- blocker or next action"
        ].join("\n")
      );
    }
  }

  if (cfg.requireFreshRunlog !== false && !hasFreshRunlog) {
    block(
      [
        "AutoGoal requires a fresh RUNLOG.md update before stopping.",
        "Update .claude/RUNLOG.md with evidence, verification commands, exit codes, git status, blocker, and next action.",
        "Then show the updated summary in the conversation."
      ].join("\n")
    );
  }

  if (cfg.requireGitStatus) {
    const lastAssistant = input.last_assistant_message || "";
    if (!/git status|git diff|working tree|工作区/i.test(lastAssistant)) {
      block(
        "AutoGoal requires git status or git diff evidence in the final message before stopping. Run git status --short and summarize intentional changes."
      );
    }
  }

  // 达标，自动关闭 autogoal
  if (cfg.autoClear !== false) {
    cfg.active = false;
    cfg.completedAt = new Date().toISOString();
    fs.writeFileSync(autogoalPath, JSON.stringify(cfg, null, 2));
  }

  process.exit(0);
}

main().catch((err) => {
  // Hook 出错时不要把 Claude 卡死，只记录到 stderr。
  console.error(String(err && err.stack ? err.stack : err));
  process.exit(0);
});
```

加权限：

```bash
chmod +x .claude/hooks/autogoal-stop.mjs
```

官方也提醒：Stop hook 如果一直 block，会触发 block cap；默认连续 block 过多时 Claude Code 会 override。文档建议读取 `stop_hook_active` 并在二次触发时放行，避免死循环。([Claude Code][3])

---

## 5. 自定义 slash command：`.claude/skills/autogoal/SKILL.md`

Claude Code 现在把 custom commands 合并进 skills：`.claude/commands/deploy.md` 和 `.claude/skills/deploy/SKILL.md` 都能创建 `/deploy`；skill 的目录名就是命令名，参数用 `$ARGUMENTS` 传入。([Claude Code][4])

创建：

```bash
mkdir -p .claude/skills/autogoal
```

写入 `.claude/skills/autogoal/SKILL.md`：

````md
---
name: autogoal
description: Start a custom AutoGoal loop controlled by .claude/autogoal.json and the project Stop hook.
disable-model-invocation: true
allowed-tools: Bash(node *) Bash(cat *) Bash(mkdir *) Bash(git status *) Read Write Edit
---

Start AutoGoal for this session.

Arguments from user:

```text
$ARGUMENTS
````

First, create or update `.claude/autogoal.json` with this schema:

```json
{
  "active": true,
  "mode": "queue",
  "goal": "$ARGUMENTS",
  "maxTurns": 20,
  "requireFreshRunlog": true,
  "runlogFreshMinutes": 45,
  "requireGitStatus": true,
  "autoClear": true,
  "createdAt": "<current ISO timestamp>"
}
```

Then do the following:

1. Read `.claude/QUEUE.md`, `.claude/RUNLOG.md`, and `.claude/BLOCKED.md` if they exist.
2. If `.claude/QUEUE.md` is missing or empty, create it from the user's AutoGoal argument.
3. Work only on the first unchecked queue item.
4. Before any stop, update `.claude/RUNLOG.md` with:

   * task item
   * changed files
   * verification commands
   * exact exit codes
   * git status
   * blocker or next action
5. Do not claim completion unless the Stop hook requirements are satisfied.

````

用法：

```text
/autogoal 完成当前 repo 的 P0 修复；每轮只做 QUEUE.md 第一项；必须跑 tsc/vitest；失败写 BLOCKED.md
````

---

## 6. 如果你想更像 `/goal`：用 prompt-based Stop hook

上面那种是**确定性 command hook**，适合你的“Agent runtime / Codex 审查 / 长跑工程”风格。

如果你想更接近内置 `/goal`，可以直接用 `type: "prompt"`：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are AutoGoal evaluator. Decide whether Claude may stop. If .claude/autogoal.json is not active based on the visible conversation, return {\"ok\": true}. If AutoGoal is active, check whether the conversation shows clear evidence that the goal is complete: verification commands, exit codes, RUNLOG update, git status, and no unchecked queue items. If complete, return {\"ok\": true}. Otherwise return {\"ok\": false, \"reason\": \"specific next action Claude must take\"}. Return JSON only."
          }
        ]
      }
    ]
  }
}
```

官方 hooks guide 也给过类似例子：Stop hook 用 `type: "prompt"` 判断任务是否完成；返回 `{"ok": false, "reason": "..."}` 时，Claude 会继续工作并把 reason 当作下一步指令。([Claude Code][3])

但我不建议你只用 prompt hook，因为它容易“看起来合理但没真的验证”。你的场景更适合：

```text
Command Stop hook = 确定性 gate
Prompt Stop hook = 语义判断补充
Agent Stop hook = 需要读文件/跑测试时再用
```

官方也说 prompt hook 是单轮模型判断；agent hook 则会 spawn subagent，可以读文件、grep、用工具验证，但仍是实验性能力。([Claude Code][3])

---

## 7. 最强版本：command gate + prompt evaluator 双层

你可以这样配：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node ${CLAUDE_PROJECT_DIR}/.claude/hooks/autogoal-stop.mjs",
            "timeout": 20,
            "statusMessage": "AutoGoal deterministic gate..."
          },
          {
            "type": "prompt",
            "prompt": "Evaluate whether the assistant's final message provides enough evidence to stop under AutoGoal. Require explicit verification commands, exit codes, git status, RUNLOG update, and no vague claims. Return {\"ok\": true} only if the evidence is sufficient; otherwise return {\"ok\": false, \"reason\": \"specific missing evidence and next action\"}. JSON only.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

这个比较接近你想要的“加强版 `/goal`”：

```text
command hook：检查状态文件、队列、RUNLOG、git evidence
prompt hook：判断最后一轮是否在语义上真的完成
Stop block：继续推进
```

---

## 8. 最关键的限制

你不能真正新增一个和内置 `/goal` 完全同级的 native command，除非 Anthropic 开放内部 command API。你能做的是：

```text
/custom skill command
+ persistent Stop hook
+ autogoal state file
```

这已经足够实现 90% 的 `/goal` 行为，而且比内置 `/goal` 更可控。

我会建议你最后把命令设计成这几个：

```text
/autogoal <目标>      开启自定义 goal
/autogoal-status      读取 autogoal.json / RUNLOG / QUEUE
/autogoal-clear       active=false
/autogoal-hard        开启更严格 gate：必须测试、git status、RUNLOG、Codex review
```

实际工程上，**固定 Stop hook + 状态文件** 是最稳的。不要每次动态改 `.claude/settings.local.json`；那样容易造成 hook 残留、递归、旧 goal 干扰新 session。

[1]: https://code.claude.com/docs/en/goal "Keep Claude working toward a goal - Claude Code Docs"
[2]: https://code.claude.com/docs/en/hooks "Hooks reference - Claude Code Docs"
[3]: https://code.claude.com/docs/en/hooks-guide?utm_source=chatgpt.com "Automate actions with hooks - Claude Code Docs"
[4]: https://code.claude.com/docs/en/skills?utm_source=chatgpt.com "Extend Claude with skills - Claude Code Docs"
