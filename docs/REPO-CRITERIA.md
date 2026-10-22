# DRAFT — K2 Trial-Repo Selection Criteria

Status: DRAFT — becomes binding only when committed in `t003-prereg`.
Purpose: reviewer D's rule requires repo selection by *fixed, queryable
criteria frozen before selection*, so that the trial repo cannot be
cherry-picked to favor ARM C. Every criterion below is stated with its
mechanical query or measurement. IMPLEMENTATION-PLAN.md constraints
honored: mid-size, actively developed, OSS service, real test suite,
not owned by the thesis author; Verifier reserved for K1/K4.

## A. Hard criteria (all must pass; each mechanically checkable)

| # | Criterion | Threshold | How measured |
|---|---|---|---|
| A1 | Primary language | C# ≥ 80% of non-test source | GitHub language stats / cloc |
| A2 | Size | 30k–150k LOC in `src` (excl. tests, generated, vendored) | cloc on clean clone |
| A3 | Shape | Deployable service or application (not a library, CLI tool, or sample/template) | Repo description + presence of a hostable entry point |
| A4 | Activity | ≥ 20 commits by ≥ 3 distinct authors in the last 12 months | git log |
| A5 | Post-cutoff activity | ≥ 10 non-trivial commits after the agent model's published training cutoff | git log vs published cutoff date |
| A6 | Test suite | Test LOC ≥ 15% of src LOC AND tests runnable headless from a clean clone | cloc + one scripted run |
| A7 | CI | A CI configuration exists and the default branch is green at fork time | CI config file + badge/API |
| A8 | Buildable | Clean clone builds and tests pass locally in ≤ 30 min without proprietary services (external deps mockable or containerized) | One timed, scripted attempt; failure disqualifies |
| A9 | License | OSI-approved permitting fork, modification, and publication of results (MIT, Apache-2.0, BSD, MPL-2.0) | LICENSE file |
| A10 | Independence | Zero commits, issues, or PRs by the thesis author or K2 operators | git log + GitHub search |
| A11 | Elicitable intents | ≥ 24 candidate intents per OPERATIONAL-DEFINITIONS §1 (each with a statable violating observation), sourced from the repo's own documented intentions | Elicitation pass over ADRs, architecture docs, CONTRIBUTING, maintainer review comments; count logged |

## B. Soft criteria (tie-breakers among passing candidates, applied in order)

1. **Lower fame** — fewer GitHub stars preferred (contamination proxy:
   the agent model is less likely to have memorized the codebase).
2. **Richer documented intentions** — more A11 candidates above 24.
3. **Domain legibility for auditors** — business/infra domain a
   non-specialist can judge (favor invoicing/API/integration over e.g.
   codec internals).

## C. Selection procedure (deterministic, logged)

1. Freeze this file in `t003-prereg`.
2. Build the candidate list from a fixed GitHub search (query string
   frozen here at prereg time), ordered deterministically (ascending
   repo creation date).
3. Walk the list in order; evaluate A1–A11; **first full pass wins**,
   after B-tie-breaking only among candidates evaluated in the same
   batch of 10.
4. Log every rejected candidate with the first criterion it failed
   (no silent discards — the rejection log is part of the prereg
   evidence).

## D. Open decision — must be resolved BEFORE freeze

OPERATIONAL-DEFINITIONS §1 requires intents "elicited from the
repository owner". For a fork of a third-party OSS repo, three readings:

- (a) contact the upstream maintainer and elicit directly (strongest;
  adds schedule risk);
- (b) treat the repo's own documented statements (ADRs, CONTRIBUTING,
  architecture docs, review comments) as the owner's recorded
  intentions, mined and sealed verbatim with source links;
- (c) amend §1 before freeze.

Default proposal: (b), with (a) attempted in parallel and used if the
maintainer responds before seal. This choice must be committed in the
prereg; deciding it after seeing candidate repos would reopen the
cherry-picking door this document exists to close.

## E. Explicitly rejected alternatives

- **Constructed/synthetic codebase** — rejected: (i) author-built code
  is unconsciously tailored to ARM C (the self-grading objection, CR1
  adjacent); (ii) a repo small enough to construct is small enough for
  the agent to comprehend fully, which removes the comprehension-gap
  phenomenon under measurement; (iii) invented intents lack the history
  that makes intent maintenance hard — the experiment would test a
  theater version of the problem.
- **Verifier or any author-owned repo** — rejected per reviewer C's
  double-duty warning and A10.
- **Top-tier famous OSS (e.g. >20k stars)** — disfavored via B1:
  training-set contamination artificially closes the comprehension gap.
