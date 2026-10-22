# Trial-Repo Selection Log (pilot)

Date: 2026-10-22. Criteria: [REPO-CRITERIA.md](REPO-CRITERIA.md).

Method note (honesty): for the pilot, the candidate pool was assembled
from a GitHub API search (`language:C# stars:200..5000 pushed:>2026-08`)
plus a knowledge-based list of known mid-size C# OSS services, then
evaluated against the A-criteria. The fully deterministic frozen-query
walk (procedure §C) is reserved for the blinded study. Every rejection
is logged below with the first criterion failed.

## Evaluation

| Candidate | Stars | License | 12m commits/authors | src LOC | test % | Verdict |
|---|---|---|---|---|---|---|
| Squidex/squidex | 2 511 | MIT | 67 / 8 | 116k | 68% | **PASS — selected** |
| btcpayserver/btcpayserver | 7 817 | MIT | 100+ / 6 | 103k | 33% | PASS — runner-up (B1 fame, heavier A8 env) |
| ShokoAnime/ShokoServer | 779 | MIT | 100+ / 3 | 304k | 27% | REJECT A2 (>150k LOC) |
| AccountGo/accountgo | 440 | MIT | 100+ / 7 | 21k | 18% | REJECT A2 (<30k LOC) |
| CervantesSec/cervantes | 450 | ? | 100+ / 1 | — | — | REJECT A4 (1 author) |
| simplcommerce/SimplCommerce | 4 413 | Apache-2.0 | 15 / 6 | — | — | REJECT A4 (<20 commits) |
| PiranhaCMS/piranha.core | 2 198 | MIT | 25 / 3 | — | — | REJECT A3 (framework, not deployable service) |
| oqtane/oqtane.framework | 2 259 | MIT | 100+ / 4 | — | — | REJECT A3 (framework) |
| Ombi-app/Ombi | 4 105 | GPL-2.0 | — | — | — | REJECT A9 (license) |
| EdiWang/Moonglade | 535 | GPL-3.0 | — | — | — | REJECT A9 |
| Jackett/Jackett | 16 237 | GPL-2.0 | — | — | — | REJECT A9 (and B1 fame) |
| Pryaxis/TShock | 2 898 | GPL-3.0 | — | — | — | REJECT A9 |
| duplicati/duplicati | 15 156 | NOASSERTION | — | — | — | REJECT A9 (unclear license; B1 fame) |
| smartstore/Smartstore | 1 736 | AGPL-3.0 | — | — | — | REJECT A9 |

LOC counted on shallow clones: non-empty lines in `*.cs`, excluding
`obj/`, `bin/`, migrations; paths containing "test" counted as test LOC.

## Selected: Squidex (headless CMS, ASP.NET Core + MongoDB)

Passes A1 (C# backend; the 66% GitHub figure includes the Angular
frontend — backend-only LOC dominates), A2 (116k), A4 (67/8), A6 (68%),
A7 (GitHub Actions present), A9 (MIT), A10 (no thesis-author commits in
history sampled). Tie-breakers: ~3× lower fame than runner-up (B1),
legible domain (B3), lighter headless build (MongoDB via container).

## Final gate results (2026-10-22) — ALL PASS, Squidex selected

- **A5 PASS**: 24 commits since 2026-06-01.
- **A7 PASS via fork point**: master HEAD is red as of 2026-10-22 (the
  two commits pushed that day broke the Dev workflow), but the branch
  was green continuously before that. **Fork point fixed at the last
  green commit: `829c2b94ee1119f91dfcc73ed552938df39c2cc3`
  (2026-10-13)** — the last SHA whose full Dev workflow succeeded.
- **A8 PASS**: clean shallow clone + full backend build (Release,
  .NET 10): **~6 minutes**, 0 errors. Filtered unit-test run
  (`Category!=TestContainer&!=MongoOnly&!=NotAutomated`): 70 s,
  4 547 passed. 159 initial failures were all environment artifacts in
  three classes, each with a standard remedy:
  1. locale (machine uses decimal comma) — fixed by
     `DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1`; verified: Core.Tests
     went 1311/1312 → 1312/1312;
  2. missing ffmpeg binary (asset metadata tests) — installable;
  3. DB/Azure/SMTP-bound tests — containerized in upstream CI, excluded
     from the headless baseline.
  Experiment baseline: invariant culture + the category filter above.
- **A11 PASS**: 28 candidate intents (≥24 required) —
  [INTENT-CANDIDATES.md](INTENT-CANDIDATES.md). Includes a field
  observation: official docs still list Orleans; the backend has zero
  Orleans references — pre-existing documentation drift in the trial
  repo itself.

Runner-up (unused): btcpayserver/btcpayserver.
