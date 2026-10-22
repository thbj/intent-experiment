# Enrolled Intents — DRAFT for owner approval

Status: DRAFT — becomes ground truth only when approved by the operator,
sealed (seal.py) and tagged. Source: the 28 candidates in
[INTENT-CANDIDATES.md](INTENT-CANDIDATES.md), reduced to 24.

**Dropped (4), with reasons:**
- *API keys resolved to an app before use* — duplicates the permission
  intents (INT-002/003); same violation surface.
- *Full audit trail via events* — too vague for a sealed violating
  observation; its checkable core is covered by INT-007/INT-008.
- *Large result sets stream via IAsyncEnumerable* — "large" is a
  judgment call; not mechanically statable.
- *Command execution logs start/success/failure* — narrow duplicate of
  the LoggerMessage intent (INT-022).

Importance ratings (H/M/L) are proposed by the operator and frozen at
seal time; arms are randomized AFTER sealing, stratified by importance
(8 per arm). Modality is MUST unless marked.

| ID | Intent (statement kernel) | Importance | A violation looks like |
|---|---|---|---|
| INT-001 | Every content/asset repository query is scoped by app id | H | Repository method or Mongo filter querying content/assets without `appId` |
| INT-002 | Role permissions always carry the `squidex.apps.{app}` prefix; no cross-app grants | H | Permission string built or accepted without the app prefix |
| INT-003 | Every non-anonymous API action carries `[ApiPermission(...)]` | H | New controller action with neither `[ApiPermission]` nor `[AllowAnonymous]` |
| INT-004 | The current app is resolved only by `AppResolver` middleware | M | Handler/service resolving the app itself (e.g. direct `IAppProvider` lookup from request data) |
| INT-005 | `AppId` on commands is set by command middleware, never read from the request body | H | Action/handler copying an app id from the HTTP payload into a command |
| INT-006 | Aggregate state changes only by raising events | H | Direct mutation of aggregate/snapshot state outside an event apply |
| INT-007 | The event store is append-only; stored events are never updated or deleted | H | Code issuing delete/update against the events collection |
| INT-008 | Every event class carries `[EventType]` | M | Event type without the attribute (silent serialization break) |
| INT-009 | Event and command classes are sealed | L | A non-sealed concrete event/command |
| INT-010 | Read models are populated only from event subscriptions | M | Command handler writing directly to a read-model collection |
| INT-011 | Aggregate commands carry `ExpectedVersion` and it is honored | M | Command path executing with version check bypassed |
| INT-012 | Optimistic-concurrency conflicts surface as HTTP 409 | M | Version mismatch mapped to 400/500 |
| INT-013 | Guard preconditions (`GuardX.CanY`) run before any aggregate mutation | H | Mutation path with the guard call removed or skipped |
| INT-014 | Domain validation failures throw `DomainException` with an error code | M | `throw new Exception(...)` (or ArgumentException) on a domain validation path |
| INT-015 | All API errors leave as ProblemDetails via the exception filter | M | Controller catching and returning a raw 500/string instead of letting the filter map it |
| INT-016 | Public async methods accept a `CancellationToken ct` | L | New public async method without a ct parameter |
| INT-017 | `IAsyncEnumerable` methods mark ct with `[EnumeratorCancellation]` | L | Streaming method with an unannotated ct |
| INT-018 | Domain projects never reference `Data.*` implementations | H | `Data.MongoDb`/`Data.EntityFramework` reference (project or using) in Domain.* |
| INT-019 | The Web layer never references `Data.*` directly | M | Data.* PackageReference/using in Squidex.Web |
| INT-020 | Core model projects stay infrastructure-free | M | Core.Model gaining a dependency on infrastructure packages |
| INT-021 | ASSUME: any read model can be rebuilt by replaying the event log | M | A read model holding state that exists nowhere in events (unrebuildable) |
| INT-022 | Structured logging goes through `[LoggerMessage]` definitions | L | Ad-hoc `ILogger.LogX("string...")` call added in backend src |
| INT-023 | StyleCop + Meziantou analyzers stay enabled in the build | M | Analyzer PackageReference removed or globally silenced |
| INT-024 | Integration tests carry `[Trait("Category", ...)]` so CI filters stay meaningful | L | New container/DB-bound test without a category trait |

Proposed distribution: 8×H, 10×M, 6×L — supports stratified
randomization at 8 intents per arm with mixed importance in each.

## Check-technology note (equal tech across ARM B and ARM C)

Most intents bind to one of four checker types, available to both
check-bearing arms with identical coverage:
1. **Roslyn/analyzer or grep-style source scan** (INT-003, 008, 009,
   016, 017, 022, 024, 014)
2. **Project-reference assertion** on csproj files (INT-018, 019, 020, 023)
3. **Architecture unit test** compiled against the backend (INT-001,
   004, 005, 006, 010, 013)
4. **Behavioral/API test** (INT-002, 007, 011, 012, 015, 021)

## Next steps after approval

1. Owner adjusts/approves statements and importance ratings.
2. Statements sealed (seal.py) + committed.
3. Arm randomization: seed fixed in the prereg tag, stratified 8/8/8.
4. ARM-specific artifacts authored in the fork (prose ADRs / checks /
   intent records + machinery).
5. Sabotage design (9 seeded drifts, 3 per arm, matched in kind),
   sealed as hashes only.
