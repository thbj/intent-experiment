# intent-experiment

A small, disposable harness for piloting one question:

> Do intentions that are **bound to mechanical consequences** (checks,
> reference integrity, red-proofs, an expiring deviation ledger) drift
> less under AI-agent maintenance than intentions kept as prose or as
> bare checks?

This repository contains the experiment machinery only — no product
code, no platform. Design background and the full three-arm experiment
protocol live in the (currently private) research workspace; the
criteria for selecting the trial repository are in
[docs/REPO-CRITERIA.md](docs/REPO-CRITERIA.md).

## Status: unblinded solo pilot

This is a **pilot run by the thesis author**, openly stated:

- No independent blinded auditors. Human-judgment outcomes (notably
  prose-arm conformance) are therefore **not validly measurable here**
  and are reported as `not measurable solo`.
- Primary outcomes are restricted to **mechanical observations**: CI
  logs (which arm's machinery went red on which seeded drift), agent
  transcripts, and the work/cost log.
- Interpretation rule, fixed in advance: a **negative** result (the
  bound arm shows no detection advantage despite author bias) is a
  strong kill signal; a **positive** result is weak evidence that only
  justifies the blinded study. See
  [docs/PILOT-PROTOCOL.md](docs/PILOT-PROTOCOL.md).

## Layout

```
intents/            one YAML record per enrolled intention (ARM C form)
checks.yaml         check registry: id -> run command + red-proof command
deviations.yaml     deviation ledger (owner + expiry, CI-enforced)
sample/             tiny self-test target so the harness can be exercised
experiment/         the scripts (run_checks, ci_intent_check, seal, worklog, cost_report)
experiment/tests/   golden tests for the harness itself
docs/               repo-selection criteria, pilot protocol
```

## Usage

```bash
# run the registered checks and write the run manifest
python3 experiment/run_checks.py

# validate the intent layer (schema, dangling refs, executed-check
# cross-check, vacuity re-proofs, ledger expiry, EXCEPTED reporting)
python3 experiment/ci_intent_check.py

# harness self-tests
python3 -m unittest discover -s experiment/tests

# seal ground truth before a run / verify afterwards
python3 experiment/seal.py seal   intents/*.yaml checks.yaml deviations.yaml
python3 experiment/seal.py verify

# work logging and cost report
python3 experiment/worklog.py start T012 "seed drift in billing"
python3 experiment/worklog.py stop  T012
python3 experiment/cost_report.py
```

Both `run_checks.py` and `ci_intent_check.py` exit non-zero on failure,
so a CI pipeline is just those two calls in sequence.

## Honesty rules

1. The design (intents, checks, red-proofs, thresholds) is committed and
   tagged **before** any measured run; post-tag edits void the affected
   comparison.
2. Everything the harness cannot measure validly in solo mode is
   labeled, not estimated.
3. Results are published regardless of outcome.
