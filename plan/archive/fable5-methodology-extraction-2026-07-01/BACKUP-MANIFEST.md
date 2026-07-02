# Fable5 Methodology Extraction — Backup + Disposition Manifest

> Archived 2026-07-02. Source workspace: `/home/lingxufeng/cli/test/` (kept intact; this is the durable
> git-tracked copy). This folder is the full structured audit of Fable 5's research methodology, produced to
> **expand Research-OS**. Below is exactly what was promoted into the plugin vs. what is archived here as
> provenance — decided by the anti-loop rule (promote only what adds a decision boundary the core loop does
> not already gate; do not rename an existing operator).

## PROMOTED → research-os v0.6.0 (github.com/CrepuscularIRIS/research-os)
Three Layer-2 wrap skills + commands (each adds a distinct decision boundary + output schema):
| Source doc here | Became | Decision boundary it adds |
|---|---|---|
| `epistemic-calibration.md` | `/epistemic-calibration` | evidence grade A–E before promotion (novelty-by-memory guard) |
| `irreversible-decision-audit.md` | `/irreversible-decision-audit` | commitment reversibility → PROCEED/DELAY/RESCOPE/BLOCK |
| `artifact-acceptance-review.md` | `/artifact-acceptance` | deliverable shippability → SHIP/REVISE/HOLD/KILL |

## FOLDED (not a new skill — added into an existing one)
| Source doc | Where it went | Why not a skill |
|---|---|---|
| `agent-governance.md` | its two sharp bits (**cold-start audit packet**, **agreement illusion → stance-separated prompts**) folded into `/adversary`'s invariant section | agent-governance IS the one invariant + the "Pro generates · Opus operates · Codex checks" engine division — a standalone skill would be renaming |

## NOT PROMOTED — archived here as provenance
| Doc(s) | Reason |
|---|---|
| `opus-skill-drafts.md` "Layer 1" (stress-point-scan, object-deletion-test, occupancy-hypothesis, minimum-falsifier, rescope-or-kill, failure-conversion, cross-domain-enrich) | already the core 7 commands (`/prospect` `/forge` `/prereg` `/adversary` `/autopsy`) — promoting = renaming |
| `context-compression-state.md` | a working-memory utility, not a research gate; useful reference, held rather than shipped as a command (its "don't re-open killed regions" discipline is already `/compass` + tree-discipline) |
| `cross-domain-operator-transfer.md` | out of scope for the research loop core (product/business transfer is a different use case) |
| `executable-enrich-protocol.md`, `meta-skill-expansion-guide.md`, `research-os-doc-index.md` | design/index docs for this extraction |
| the extraction PROMPTS (`fable-public-procedure-extraction.md`, `fable-part-followup-prompts.md`, `fable-to-opus-operator-library.md`, `opus-distillation-prompt.md`, `fable-opus-calibration-suite.md`, `fable5-meta-distillation-master-prompt.md`, `fable5-research-methodology-tradeoff-prompt.md`) | the process used to extract the methodology — provenance, not skills |
| `fable-research-audit/`, `fable5-methodology-audit/` | the raw multi-stage audit outputs (evidence standards, action-selection, kill/rescope, commitment risk, governance, artifact acceptance, cross-domain, execution boundaries, calibration cases, final methodology) — the source material the promoted skills distill |
| `enrich.md` | a copy of the methodology already in the repo root |

## Anti-loop note
The extraction's own rule: *stop adding workflow when the next document adds no new kill condition, output
schema, or decision boundary.* Of ~20 candidate capabilities, 3 were promoted and 1 was folded — the rest
are kept for reference, not shipped, to avoid the monotone-accretion failure the v0.5 rebuild diagnosed.
