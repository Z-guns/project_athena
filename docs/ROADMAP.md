# Project Athena Roadmap

This roadmap sequences Project Athena as small, testable capabilities. A phase is complete only when
its success criteria are met; later phases may refine earlier infrastructure without bypassing the
architectural boundaries in `docs/ARCHITECTURE.md`.

## Phase 1: Foundation — Completed

### Goal

Establish a production-minded Python and FastAPI foundation for incremental development.

### Deliverables

- Python 3.12 and 3.13 project metadata and dependency management.
- Environment-backed, strongly typed application settings.
- Structured JSON and development console logging.
- FastAPI application factory, lifespan management, and CORS middleware.
- Versioned root API router and liveness endpoint.
- Initial architecture and delivery documentation.

### Success Criteria

- The application can be configured without hard-coded credentials.
- Invalid or unsafe production settings fail during startup.
- Logging is readable locally and machine-parseable in production.
- `GET /api/v1/health` returns a validated successful response.
- The engineering boundaries for future phases are documented.

## Phase 2: Database & Persistence

### Goal

Provide reliable asynchronous persistence while keeping database concerns outside the domain.

### Deliverables

- Async SQLAlchemy engine and session lifecycle.
- Alembic configuration and an initial migration baseline.
- Unit-of-work and repository abstractions.
- PostgreSQL health/readiness integration.
- Transaction rollback and persistence integration tests.

### Success Criteria

- Database sessions are created, committed, rolled back, and closed predictably.
- Migrations apply cleanly to an empty database and can be rolled back safely.
- Domain and application layers do not depend on SQLAlchemy models or sessions.
- Persistence tests run against an isolated PostgreSQL database.
- Readiness reports database unavailability without exposing sensitive details.

## Phase 3: Authentication & Users

### Goal

Establish secure user identity, authentication, and authorization boundaries.

### Deliverables

- User domain model and persistence mapping.
- Password hashing and credential validation.
- JWT access-token issuance and verification.
- Registration, login, current-user, and token lifecycle endpoints.
- Authorization dependencies and security audit events.

### Success Criteria

- Passwords are never stored or logged in plaintext.
- Invalid, expired, or tampered tokens are rejected consistently.
- Protected endpoints require an authenticated user.
- Authentication behavior is covered by unit, integration, and API tests.
- Security responses avoid user enumeration and sensitive error disclosure.

## Phase 4: Task Manager

### Goal

Enable users and agents to create, prioritize, track, and complete structured work.

### Deliverables

- Task aggregate, lifecycle rules, priorities, and status transitions.
- Task commands, queries, repositories, and API endpoints.
- Ownership and authorization rules.
- Due-date, filtering, ordering, and pagination support.
- Task domain events for downstream integrations.

### Success Criteria

- Invalid task transitions are rejected by domain rules.
- Users can access and mutate only authorized tasks.
- Listing behavior is deterministic, filtered, and paginated.
- Task use cases are testable without FastAPI or PostgreSQL.
- Task events are emitted once per successful state transition.

## Phase 5: Memory Engine

### Goal

Store and retrieve durable, attributable memories for users and agents.

### Deliverables

- Memory model with source, ownership, scope, and retention metadata.
- Ingestion, retrieval, update, and deletion use cases.
- Embedding and vector-store ports with an initial adapter.
- Semantic search with metadata filtering.
- Retention, deduplication, and privacy controls.

### Success Criteria

- Every memory is attributable to a source and owner.
- Semantic retrieval respects authorization and scope filters.
- Provider adapters can be replaced without changing memory use cases.
- Duplicate and expired memories are handled deterministically.
- Deletion removes or tombstones all searchable representations as designed.

## Phase 6: Research Engine

### Goal

Produce traceable research artifacts from multiple sources and bounded workflows.

### Deliverables

- Research request, source, finding, and report models.
- Search, retrieval, extraction, synthesis, and citation ports.
- Asynchronous research workflow with cancellation and timeouts.
- Source provenance and confidence metadata.
- Research API and persistence integration.

### Success Criteria

- Report claims can be traced to recorded sources.
- Failed sources do not silently become successful findings.
- Workflows enforce configured time, cost, and source limits.
- Cancellation leaves research jobs in a consistent state.
- Core synthesis behavior is testable with deterministic provider fakes.

## Phase 7: LLM Abstraction Layer

### Goal

Offer provider-neutral, observable, and policy-controlled access to language models.

### Deliverables

- Common chat, structured-output, embedding, and streaming interfaces.
- OpenAI, Gemini, and Anthropic adapters as required by use cases.
- Model capability registry and routing policy.
- Timeout, retry, rate-limit, and error-normalization behavior.
- Prompt versioning, token usage, and cost metadata.

### Success Criteria

- Application use cases do not import provider SDK types.
- Supported providers pass the same contract test suite.
- Structured responses are validated before entering the domain.
- Retries occur only for explicitly safe and transient failures.
- Usage and latency are observable without logging prompts or secrets by default.

## Phase 8: Browser Automation

### Goal

Provide controlled browser capabilities for research and approved agent actions.

### Deliverables

- Browser session, navigation, extraction, and interaction ports.
- Playwright adapter with lifecycle and resource limits.
- Domain allowlists, action policies, and timeout controls.
- Artifact capture for permitted screenshots and traces.
- Browser job API and audit events.

### Success Criteria

- Browser processes and contexts are closed after success, failure, or cancellation.
- Navigation and actions obey explicit domain and authorization policies.
- Sensitive values are redacted from logs and stored artifacts.
- Automation failures produce normalized, actionable errors.
- Critical browser workflows pass repeatable integration tests.

## Phase 9: Social Platform Adapters

### Goal

Integrate supported social platforms behind stable, policy-aware application contracts.

### Deliverables

- Shared publishing, reading, analytics, and account capability contracts.
- Initial adapters for selected Instagram, TikTok, and X capabilities.
- Credential storage and token refresh boundaries.
- Rate-limit handling, idempotency, and platform error translation.
- Approval workflow and audit trail for external actions.

### Success Criteria

- Platform-specific payloads remain inside adapters.
- Duplicate requests do not create duplicate external actions where preventable.
- Expired credentials and rate limits are handled predictably.
- Publishing actions require explicit policy and user authorization.
- Each adapter passes capability-specific contract and sandbox tests.

## Phase 10: Orchestrator

### Goal

Coordinate multi-step agent workflows across Athena's bounded contexts safely and transparently.

### Deliverables

- Workflow, step, execution, and policy models.
- Planner and executor interfaces with deterministic state transitions.
- Tool registry backed by explicit application capabilities.
- Pause, resume, cancel, retry, and compensation behavior.
- Human approval gates and execution audit history.

### Success Criteria

- Every external or destructive action passes an authorization policy.
- Workflow state can recover after process interruption.
- Retries and resumptions do not duplicate completed side effects.
- Users can inspect what ran, why it ran, and what it changed.
- Orchestration depends on public module contracts rather than module internals.

## Phase 11: Observability & Monitoring

### Goal

Make application health, performance, failures, and resource usage visible and actionable.

### Deliverables

- Correlation identifiers across HTTP requests and background workflows.
- Metrics for latency, errors, dependencies, queues, and model usage.
- Distributed tracing across supported infrastructure boundaries.
- Liveness, readiness, and dependency health endpoints.
- Dashboards, alert rules, runbooks, and retention policies.

### Success Criteria

- Operators can trace a failed request or workflow across module boundaries.
- Alerts identify user-impacting conditions with actionable context.
- Sensitive fields are consistently excluded or redacted.
- Health checks distinguish process availability from dependency readiness.
- Observability overhead remains measured and within agreed limits.

## Phase 12: Production Deployment

### Goal

Deploy Athena through a secure, repeatable, reversible production delivery process.

### Deliverables

- Container image and hardened runtime configuration.
- Environment provisioning and secret-management integration.
- Automated lint, type-check, test, migration, and deployment pipeline.
- Reverse proxy, TLS, scaling, backup, and disaster-recovery configuration.
- Deployment, rollback, incident-response, and maintenance runbooks.

### Success Criteria

- A clean environment can be provisioned and deployed from version-controlled definitions.
- Releases require passing quality and security gates.
- Database migrations and application releases have tested rollback procedures.
- Backups are encrypted and restoration is verified regularly.
- Production configuration contains no placeholder secrets or development-only behavior.
- Service-level objectives, ownership, and incident escalation paths are documented.
