# Pilot Protocol (unblinded solo run)

Status: governs the pilot only. The full three-arm blinded protocol
lives in the research workspace (T003) and is NOT superseded by this
document.

## What this pilot is

A solo, unblinded dry run of the three-arm structure trial, executed by
the thesis author, to (a) debug the machinery, (b) get an effect-size
feel, (c) produce honest preliminary numbers. It deliberately trades
validity for speed, and says so.

## Fixed interpretation rule (decided before any run)

- **Negative result** (ARM C machinery shows no detection advantage
  over ARM B's bare checks on the seeded drifts): STRONG signal — the
  author is maximally biased toward C, and C still failed to show
  value. Treat as a live kill indication per GO-NO-GO K2-1.
- **Positive result**: WEAK evidence. Justifies running the blinded
  study with independent auditors; proves nothing by itself.

## Measured outcomes (mechanical only)

1. Per seeded drift: did any machinery go red, which arm, which
   mechanism (check / dangling ref / vacuity re-proof / ledger expiry),
   at which task (latency). Source: CI logs, run manifests.
2. Agent behavior on red: comply, reroute, or attempt to weaken the
   check (weakening attempts are counted — they are the B-erosion
   phenomenon). Source: transcripts.
3. Cost per arm: operator minutes (worklog.csv), agent tokens and
   iterations per task. Source: cost_report, agent logs.

## Explicitly NOT measurable solo (reported as such, never estimated)

- End-state conformance of ARM A (prose) intentions — requires judges
  who do not know the seeding ground truth.
- All borderline conformance judgments.
- Inter-rater agreement, by definition.

## Discipline retained from the full protocol

- Design, intents, checks, red-proofs and seeded-drift list are sealed
  (seal.py + a git tag) BEFORE the first measured run; post-tag edits
  void the affected comparison.
- Work is logged with worklog.py throughout.
- Results are written up and published regardless of outcome.
