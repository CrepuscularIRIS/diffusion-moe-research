# Codex-A SELECT Verdict - Research OS Command Minimalism

## Selector stance

Default skeptical. Build a standalone command only when it changes a downstream decision by binding to evidence, external competition, or durable memory. Do not build commands whose main output is persuasive prose; those are easy for the loop to game and are exactly the over-specified workflow failure the report warns about.

The governing rule I applied:

> Agents may prepare, falsify, verify, and record. Agents may not define topic value, inflate claim scope, or launder a post-hoc story into success.

## Minimal command set to build

Six commands total. This is the upper bound I would accept; fewer is acceptable if wiring pressure appears.

| Command | One-line trigger | Engine | Why it survives |
|---|---|---|---|
| `/context-bundle` | Before any nontrivial LLM dispatch; fail closed if recent negatives, forbidden assumptions, must-read paths, or hashes are missing. | Opus | Prevents repeated dead ideas and stale-context drift before the loop spends work. |
| `/exp-verify` | Immediately after each experiment run, before any number can enter RUNLOG, memory, or a claim. | Codex | Machine-checks no-mock, artifact existence, sane ranges, stale-cache risk, and whether the intervention actually fired. |
| `/reward-hack-audit` | Before promoting, banking, merging, or writing up a positive or surprising result. | Codex | Runs the material anti-Goodhart checks: min-form, per-example regression, controls, holdout, token-shuffle, metric validity. |
| `/baseline-champion` | Whenever a claim says "beats X" or makes a cross-system comparison. | Codex | Forces an independent adversary to make the baseline win; no dominance claim without this sign-off. |
| `/bank-negative` | On any kill, inconclusive run, failed reproduction, or abandoned hypothesis. | Codex | Converts failure into durable NegativeCase memory with ruled-out claims, surviving alternatives, retry conditions, and next probe. |
| `/claim-evidence-matrix` | Before paper-mode, external claim, abstract drafting, or any claim upgrade. | Codex | Every claim must map to an evidence type or be downgraded to hypothesis; this directly blocks story inflation. |

## Candidate dispositions

| Candidate | Disposition | Anti-Goodhart value | Ceremony cost | Verdict |
|---|---:|---:|---:|---|
| `/taste-gate` | PURE-HUMAN-GATE | High | Med | The Taste Card is useful only as material for a human decision; an agent-scored taste command would optimize for rubric-looking prose. ILLUSORY if automated: it looks rigorous but cannot bind topic value. |
| `/external-decision-gate` | FOLD-INTO-IDEATE | High | Low | Make "if true, who changes what decision?" a required field in `/ideate` candidate cards and promotion briefs. No separate command is needed; if the named stakeholder/action is absent, the candidate is demoted before selection. |
| `/baseline-champion` | BUILD-COMMAND | High | Med | This is one of the few L2 gates with a real adversarial substrate: an independent agent actually tries to make the opposing baseline win. It changes decisions by blocking dominance claims. |
| `/kill-reviewers` | CUT | Med | High | Four kill personas mostly produce plausible objections and duplicate reward-hack, baseline, and scope checks. ILLUSORY: unless tied to external evidence, it adds scary prose without a hard stop. |
| `/preregister` | FOLD-INTO-OPERATING-MANUAL | High | Low | Keep timestamped hypothesis, falsifier, metric, split, and go/no-go rule in RUNLOG before sealed evaluation. Do not make this a command for every experiment; the artifact is valuable, the ceremony is not. |
| `/pivot-ledger` | CUT | Med | Med | A standalone ledger is mostly narrative bookkeeping after the fact. ILLUSORY: if preregistration, RUNLOG, `/bank-negative`, and `/claim-evidence-matrix` are enforced, a separate pivot artifact changes no decision. |
| `/negative-grade` | CUT | Med | Low | The useful part is a field inside `/bank-negative`, not a command. ILLUSORY as standalone: grading a negative without capturing evidence, ruled-out space, and next probe is just relabeling. |
| `/problem-structure-extract` | FOLD-INTO-IDEATE | High | Low | This is exactly Stage-1 landscape work: problem sentence, default assumption, minimal mechanism, killer experiment, failure boundary, missing evidence, reusable principle. It should sharpen `/ideate`, not become another artifact to invoke. |
| `/claim-evidence-matrix` | BUILD-COMMAND | High | Med | This changes decisions by downgrading unsupported claims before paper-mode. It is bounded and evidence-typed, so it is less gameable than generic reviewer simulation. |
| `/reward-hack-audit` | BUILD-COMMAND | High | Med | This attacks observed failure modes with checkable artifacts: aggregate masking, metric gaming, leakage, missing controls, token-supervision confounds, and min-form bottlenecks. Run it only at promotion/merge/write-up boundaries to avoid constant drag. |
| `/exp-verify` | BUILD-COMMAND | High | Low | This is machine-checkable and catches no-op, mock, cache, artifact, and plausibility failures before a result becomes part of the research memory. It is the highest-value L1 command. |
| `/bank-negative` | BUILD-COMMAND | High | Low | NegativeCase memory prevents the loop from recycling killed directions and preserves understanding from failures. It also absorbs the useful part of `/negative-grade`. |
| `/context-bundle` | BUILD-COMMAND | High | Low | Context failures directly cause repeated bad ideas, stale assumptions, and re-litigation of dead branches. Keep it mechanical and small: recent negatives, forbidden assumptions, must-read paths, hashes, and short context. |
| `/stage-protocol` | FOLD-INTO-OPERATING-MANUAL | Med | High | Use it as an overrideable default ladder for training-heavy adapter work, not as a standalone command. ILLUSORY/dangerous if rigid: the AAR lesson is that a fixed pipeline can be worse than none when cheap de-risking wants a different path. |

## Illusory rigor flags

The main false-positive rigor risks are:

1. Automated `/taste-gate`: a taste rubric filled by the same loop is taste cosplay, not taste.
2. `/kill-reviewers`: persona panels often increase objection volume without binding to a stop condition.
3. `/pivot-ledger`: if not read by a promotion gate, it is a diary, not a constraint.
4. `/negative-grade`: a grade without evidence capture and next discriminating probe changes nothing.
5. Rigid `/stage-protocol`: a mandatory ladder can waste runs and recreate the over-specified workflow failure.

## Operating-manual folds

The manual should contain only these lightweight rules:

- Before sealed evaluation, RUNLOG must include timestamped hypothesis, falsifier, metric, split, and go/no-go rule.
- A pivot must cite the prior preregistered claim and whether results were seen before the new claim was formed.
- Adapter training may use baseline -> tune-frozen -> creative -> ablation as the default path, but the coordinator can skip stages when a cheaper falsifier exists.
- Human taste owns problem value, claim boundary, when to stop chasing score, and whether a negative result is accepted.

## Final SELECT

Build `/context-bundle`, `/exp-verify`, `/reward-hack-audit`, `/baseline-champion`, `/bank-negative`, and `/claim-evidence-matrix`.

Do not build standalone `/taste-gate`, `/external-decision-gate`, `/kill-reviewers`, `/preregister`, `/pivot-ledger`, `/negative-grade`, `/problem-structure-extract`, or `/stage-protocol`. Their useful content either belongs inside `/ideate`, the operating manual, the human gate, or the surviving evidence commands.
