# Project Athena Architecture

## Project Vision

Project Athena is a modular, AI-enabled platform for coordinating specialized agents, durable
knowledge, research, decisions, tasks, and platform interactions. The system is designed to grow
incrementally without coupling business rules to web frameworks, databases, model providers, or
automation tools.

The architecture prioritizes:

- explicit domain boundaries;
- independently testable business logic;
- replaceable infrastructure and AI providers;
- observable, secure production behavior;
- small, reviewable increments over speculative implementation.

## Architectural Style

Athena follows Clean Architecture within a modular monolith. Each business module owns its domain
model and use cases while sharing only carefully selected primitives through the shared kernel.
Modules may later be extracted into services if operational needs justify the additional cost.

Dependencies always point inward:

```text
Presentation -> Application -> Domain
Infrastructure -> Application and Domain ports
```

The domain layer has no dependency on FastAPI, SQLAlchemy, external APIs, message brokers, or other
delivery and infrastructure concerns.

## Layer Responsibilities

### Domain

The domain layer contains entities, value objects, domain services, domain events, repository
contracts, and domain exceptions. It expresses business invariants and must remain deterministic
where practical.

### Application

The application layer coordinates use cases. It defines commands, queries, handlers, transaction
boundaries, and ports required from infrastructure. It may depend on the domain, but it must not
depend on concrete adapters.

### Infrastructure

The infrastructure layer implements application and domain ports using PostgreSQL, Redis, AI
providers, browser automation, external APIs, and other technical systems. Infrastructure failures
must be translated into stable application-facing errors.

### Presentation

The presentation layer exposes use cases through FastAPI routers and request/response schemas. It
handles transport concerns such as authentication, validation, status codes, and serialization. It
must not contain business rules or issue database queries directly.

## Domain-Driven Design Boundaries

Each directory under `backend/modules` represents a bounded context. Current planned contexts are:

- orchestrator;
- memory;
- research;
- decision;
- task manager;
- journal;
- character management;
- account intelligence;
- growth engine;
- browser;
- platform agents.

A bounded context owns its language, models, persistence mappings, and public application
contracts. One context must not import another context's internal domain or infrastructure code.
Cross-context collaboration occurs through explicit application contracts, domain events, or an
integration bus.

The shared kernel is intentionally small. It may contain stable, broadly meaningful abstractions
such as base domain events, identifiers, result types, and transaction or messaging interfaces. It
must not become a miscellaneous utilities package.

## Dependency and Integration Rules

- Domain code imports only the Python standard library and approved domain-level primitives.
- Application code depends on domain abstractions, never concrete infrastructure.
- Infrastructure adapters implement inward-facing ports and are wired at the composition root.
- Presentation code calls application use cases rather than repositories or provider SDKs.
- Modules communicate through explicit contracts; private module internals remain private.
- Provider-specific models never cross adapter boundaries.
- Configuration is loaded centrally and injected where practical.
- Side effects occur at explicit boundaries and are covered by integration tests.
- Circular dependencies between modules or layers are prohibited.

## API and Composition

`backend/app.py` is the application composition root. It configures logging and middleware, manages
the FastAPI lifespan, and registers the root API router. API versioning is controlled by the
configured prefix, currently `/api/v1`.

`backend/api/router.py` composes health and future feature routers. Feature endpoints should live in
their owning bounded context and be included by the root router through an explicit registration.

Health checks must remain lightweight. Liveness should report process availability; future
readiness checks may verify required dependencies without leaking credentials or internal details.

## Data and Transactions

PostgreSQL is the authoritative relational store. SQLAlchemy models are infrastructure concerns and
must not replace domain entities. Repository interfaces belong inward; implementations belong in
infrastructure.

Transactions should align with one application use case. Cross-context consistency should prefer
domain events and eventual consistency over distributed transactions. Alembic migrations are the
only supported mechanism for production schema changes.

Redis may support caching, coordination, rate limiting, and transient messaging. It must not become
the unowned source of truth for domain state.

## AI and External Providers

OpenAI, Gemini, Anthropic, vector databases, social platforms, and Playwright are external adapters.
Application code targets provider-neutral interfaces. Adapter responsibilities include request
translation, timeouts, retries where safe, rate-limit handling, response validation, and telemetry.

Prompts and model settings are versioned artifacts. Sensitive input and credentials must never be
written to logs. Autonomous actions require explicit authorization boundaries and auditable events.

## Security and Observability

- Secrets come from environment-backed settings and are never committed.
- Production rejects placeholder secrets and debug mode.
- CORS uses an explicit allowlist; wildcard origins are not a production default.
- Authentication and authorization are enforced at transport and use-case boundaries.
- Logs are structured JSON in production and readable colored output in development.
- Logs use stable event names and contextual fields rather than interpolated prose.
- Errors exposed through APIs contain safe messages and correlation identifiers.
- Metrics and tracing may be added at infrastructure boundaries without changing domain logic.

## Testing Boundaries

- Unit tests cover domain invariants and application use cases without network or database access.
- Integration tests cover repositories, migrations, provider adapters, and module wiring.
- End-to-end tests cover a small number of critical workflows through public interfaces.
- Tests follow the same module boundaries as production code.
- External systems are replaced at defined ports, not patched through domain internals.

## Architectural Decision Policy

Significant decisions should be recorded before implementation when they affect module boundaries,
data ownership, security, deployment, or irreversible provider choices. Architecture evolves through
measured changes; new abstractions must solve a current boundary problem rather than anticipate an
unknown one.
