# Enrolled Intents — DRAFT v2 for owner approval

Status: DRAFT — becomes ground truth only when approved, sealed and
tagged. v2 after owner feedback on v1: *statements were too
implementation-technical; intents should be behavior-first*. v1 is in
git history.

Design shift in v2: each intent is stated as **observable behavior or
an owner-level architecture commitment** — what must hold — not as a
code pattern. Code patterns are *projections*: they may appear as the
check implementation, but the sealed statement and the auditors' ground
truth live at behavior level. This also lowers the auditor bar: most
verdicts can be reached by probing a running instance or reading API
test results instead of reviewing middleware internals.

Mix: 14 behavioral, 7 architectural, 3 process-level. Importance:
8 H / 12 M / 4 L (stratified randomization at 8 per arm). Modality MUST
unless marked. Check technology is equal across ARM B and C per intent.

## Behavioral intents (API-observable)

| ID | Intent | Imp. | A violation looks like |
|---|---|---|---|
| INT-001 | Tenant isolation: content, assets and settings of one app can never be read or modified using another app's credentials | H | Any request authenticated for app A returning or mutating app B data |
| INT-002 | Role boundaries hold: a client/user can perform only actions its role grants (e.g. a Reader can never modify content or schemas) | H | A Reader token successfully creating/updating content |
| INT-003 | No anonymous access to protected resources: endpoints require authentication unless explicitly configured anonymous | H | Unauthenticated request succeeding against a protected endpoint |
| INT-004 | Unpublished content is never served through the public content API | H | Draft content appearing in an unauthenticated/client content query |
| INT-005 | Data is never destroyed: deleting content keeps its history recoverable (soft delete; the event record survives) | H | A delete that physically removes events/history |
| INT-006 | Concurrent conflicting updates never silently lose a write: the later writer receives 409 | M | Second writer getting 200 and overwriting the first write |
| INT-007 | Content that violates its schema is rejected with a validation error, never stored | H | Invalid field value accepted and persisted |
| INT-008 | API errors return structured ProblemDetails with error codes — never raw stack traces or bare 500s | M | Endpoint leaking an exception message/stack trace |
| INT-009 | Every content change is visible in that content's version history | M | An update that leaves no history entry |
| INT-010 | ASSUME: any read model can be rebuilt by replaying the event log — no state exists outside events | M | A feature storing state that event replay cannot reproduce |
| INT-011 | A role defined in app X grants nothing in app Y (permissions never cross the app prefix) | M | Cross-app action succeeding via a role from another app |
| INT-012 | Resources of a deleted app are no longer accessible through the API | M | Requests against a deleted app still serving its data |
| INT-013 | Rules/webhooks fire for the content events they subscribe to | L | A matching content event producing no rule execution |
| INT-014 | Content API responses carry ETags and honor If-None-Match for caching | L | Endpoint dropping ETag behavior |

## Architectural intents (owner-level structure commitments)

| ID | Intent | Imp. | A violation looks like |
|---|---|---|---|
| INT-015 | The domain layer is storage-agnostic: no Domain project references Data.* implementations | H | Data.MongoDb/EntityFramework reference (project or using) in Domain.* |
| INT-016 | The web layer never touches storage directly — all data access goes through domain services | M | Data.* reference or direct Mongo query in Squidex.Web |
| INT-017 | Core model projects stay infrastructure-free | M | Core.Model gaining an infrastructure dependency |
| INT-018 | Aggregate state changes only by raising events (CQRS discipline) | H | Direct mutation of aggregate/snapshot state outside an event apply |
| INT-019 | The event store is append-only: no code path updates or deletes stored events | M | Code issuing update/delete against the events collection |
| INT-020 | The current app is resolved once, by middleware — business logic never resolves it ad hoc | M | Handler/service doing its own app lookup from request data |
| INT-021 | Repository contracts are app-scoped by signature: no data query API without an app id | M | New repository method querying content/assets without appId |

## Process intents (build/test discipline)

| ID | Intent | Imp. | A violation looks like |
|---|---|---|---|
| INT-022 | Static analyzers (StyleCop, Meziantou) stay enabled in the build | M | Analyzer PackageReference removed or globally silenced |
| INT-023 | Every event class is registered for serialization via [EventType] — events must survive versioning | L | New event type without the attribute (silent serialization break) |
| INT-024 | Integration tests carry [Trait("Category", ...)] so CI filters stay meaningful | L | New container/DB-bound test without a category trait |

## Check technology per intent (equal tech in ARM B and ARM C)

- **API/behavioral tests** (run against instance + Mongo container,
  reusing tools/TestSuite technology): INT-001…009, 011…014
- **Event-replay harness**: INT-010
- **Architecture tests / project-reference assertions**: INT-015…021
- **Build/source assertions**: INT-022…024

Infrastructure note: behavioral checks require a running Squidex +
MongoDB (Docker available on the pilot machine; upstream CI does the
same). Red-proof fixtures for behavioral checks are violation *commits*
(sealed) whose deployment must turn the check red.

## Dropped from v1 (beyond the four dropped from the candidate list)

Pure code-style intents (sealed classes, ct parameters,
[EnumeratorCancellation], LoggerMessage pattern, file-scoped
namespaces) — all were implementation patterns with no behavior or
owner-commitment content. Replaced by behavioral intents INT-004, 007,
009, 012, 013, 014.

## Next steps after approval

1. Owner adjusts/approves statements and importance ratings.
2. Statements sealed (seal.py) + committed.
3. Arm randomization: seed fixed in the prereg tag, stratified 8/8/8.
4. ARM artifacts authored in the fork (thbj/squidex @ 829c2b94).
5. Sabotage design (9 seeded drifts, 3 per arm, matched in kind),
   sealed as hashes only.
