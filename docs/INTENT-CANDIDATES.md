# Intent Candidates — Squidex (A11 elicitation pass)

Date: 2026-10-22. Sources: code sweep of a shallow clone (structure,
.editorconfig, analyzers, middleware, interfaces) and the official docs
(docs.squidex.io: architecture overview, permissions concept page).
Verdict: **A11 PASS** — 28 candidates with statable violating
observations, against the required 24.

These are *candidates*. The enrolled 24 get sealed statements, a
violating-observation definition, importance ratings and arm assignment
at seeding time. Status column: ENFORCED = an analyzer/filter/middleware
reacts today; CONVENTION = followed but nothing reacts (prime ARM A/B/C
material); DOC = stated in official docs.

## Multi-tenancy (apps)

| # | Intent | Violation looks like | Status |
|---|---|---|---|
| 1 | Every content/asset repository query is scoped by app id | Repository method without `DomainId appId` parameter/filter | CONVENTION |
| 2 | Role permissions are always auto-prefixed `squidex.apps.{app}` — no cross-app grants | Permission string built without the app prefix | DOC + code |
| 3 | Non-anonymous API endpoints carry `[ApiPermission(...)]` | Controller action with neither `[ApiPermission]` nor `[AllowAnonymous]` | CONVENTION (filter enforces only when attribute present) |
| 4 | Current app is resolved only by `AppResolver` middleware | Business logic looking up the app from the database itself | CONVENTION |
| 5 | `AppId` on commands is set by command middleware, never taken from request body | Handler reading AppId from the HTTP payload | CONVENTION |
| 6 | API keys are resolved to an app before use | Key accepted without app resolution step | CONVENTION |

## Event sourcing / CQRS

| # | Intent | Violation looks like | Status |
|---|---|---|---|
| 7 | Aggregate state changes only via raised events | Direct property assignment on aggregate state | CONVENTION |
| 8 | The event log is append-only; events are never deleted ("Data is never deleted") | Code deleting/updating stored events | DOC |
| 9 | Every event class carries `[EventType]` | Event class without the attribute (breaks serialization/migration) | CONVENTION |
| 10 | Event and command classes are sealed | `class X : AppEvent` that is abstract/open | CONVENTION |
| 11 | Read models are populated only from event subscriptions | Command handler writing a read-model collection directly | DOC + code |
| 12 | Commands carry `ExpectedVersion` for optimistic concurrency | Command executed ignoring version | CONVENTION |
| 13 | Concurrency conflicts surface as HTTP 409 | Version mismatch returned as 400/500 | CONVENTION |
| 14 | Full audit trail: every change historized via events | Mutation path that bypasses the event store | DOC |

## Validation and errors

| # | Intent | Violation looks like | Status |
|---|---|---|---|
| 15 | Guard preconditions run before any aggregate mutation | Mutation without `GuardX.CanY()` call | CONVENTION |
| 16 | Domain validation failures throw `DomainException` with error code | `throw new Exception(...)` in domain validation | CONVENTION |
| 17 | All API errors leave as ProblemDetails via the exception filter | Endpoint bypassing `ApiExceptionFilterAttribute` | ENFORCED |

## Async discipline

| # | Intent | Violation looks like | Status |
|---|---|---|---|
| 18 | Public async methods accept a `CancellationToken ct` | New async interface method without ct | CONVENTION (CA2016 disabled) |
| 19 | `IAsyncEnumerable` parameters use `[EnumeratorCancellation]` | Streaming method with plain ct | CONVENTION |
| 20 | Large result sets stream via `IAsyncEnumerable`, not materialized lists | `List<T>` return on an unbounded query | CONVENTION |

## Layering

| # | Intent | Violation looks like | Status |
|---|---|---|---|
| 21 | Domain projects never reference `Data.*` (MongoDB/EF) | `using Squidex.Data.MongoDb;` in Domain.Apps.Entities | CONVENTION (project refs only) |
| 22 | Web layer never references `Data.*` directly | Data.MongoDb PackageReference in Squidex.Web | CONVENTION |
| 23 | Core model stays infrastructure-free | Core.Model gaining an infra dependency | CONVENTION |

## Logging

| # | Intent | Violation looks like | Status |
|---|---|---|---|
| 24 | Structured logging via `[LoggerMessage]` partial `LogMessages` | Ad-hoc `ILogger.LogInformation(...)` string calls | CONVENTION |
| 25 | Command execution logs start/success/failure | Command middleware without the three log points | CONVENTION |

## Build/test discipline

| # | Intent | Violation looks like | Status |
|---|---|---|---|
| 26 | File-scoped namespaces everywhere | Old-style `namespace X { }` block | ENFORCED (.editorconfig) |
| 27 | StyleCop + Meziantou analyzers stay enabled in the build | Analyzer PackageReference removed or severity silenced wholesale | ENFORCED (and its removal is the classic ARM B erosion) |
| 28 | Tests carry `[Trait("Category", ...)]` so CI filters stay meaningful | New integration test without category | CONVENTION + CI |

## Field note: documentation drift already present

The official architecture docs still list **Orleans** as part of the
backend stack; the current backend has **zero Orleans references**
(checked across all csproj files and central package management). The
selected trial repo thus already exhibits the phenomenon under study —
prose architecture documentation that silently rotted while the code
moved on.

## Mix assessment for the experiment

Good spread for arm assignment: 2 currently ENFORCED (red-proofable as-is),
~22 CONVENTION (bindable with new checks of equal technology across ARM
B/C, or left as prose in ARM A), 4 DOC-sourced (ideal ARM A material —
already prose today). Multi-tenancy and event-sourcing intents are
high-importance; async/logging ones low-importance — useful for the
importance-stratified randomization.
