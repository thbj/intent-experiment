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

## Still to verify before fork is final

- A5: ≥10 non-trivial commits after the agent model's training cutoff.
- A7: default branch actually green at fork time.
- A8: clean clone builds + tests pass ≤30 min headless (timed run).
- A11: elicitation pass must yield ≥ 24 intents with statable violating
  observations (sources: external docs at docs.squidex.io, in-repo
  conventions, maintainer contact per REPO-CRITERIA.md §D).

Fallback if any fails: btcpayserver/btcpayserver, same checks.
