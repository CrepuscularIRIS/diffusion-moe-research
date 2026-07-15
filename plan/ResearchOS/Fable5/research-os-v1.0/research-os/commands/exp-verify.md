---
name: exp-verify
description: Verify a run is REAL before trusting its numbers — structural no-mock → execution exit-0 + artifact + intended-data-consumed → anti-no-op (the intervention provably FIRED). A no-op FAILS even if the metric improved; VERIFIED = real run, not real effect. Loads the `exp-verify` skill. $ARGUMENTS = script path + output dir.
disable-model-invocation: true
argument-hint: "[experiment script path + output dir]"
---
Run the `exp-verify` skill on: $ARGUMENTS
