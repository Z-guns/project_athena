# Athena AI — Backend Architecture

This document is a concise, production-ready reference for backend engineers joining Athena AI. It
describes the project's design goals, technology choices, layer responsibilities, and rules that
preserve long-term maintainability.

## 1. Vision

Athena AI is an extensible platform for composing AI-driven agents and domain-specific workflows.
The backend's mission is to enable durable, auditable automation while keeping business rules
independent from delivery frameworks, storage engines, and provider implementations. Over time the
platform should support: multi-provider AI strategies, safe autonomous actions, durable memory,
and scalable coordination of specialized agents — all while preserving testability and clear
ownership boundaries.

## 2. Technology Stack

- Python 3.13
- FastAPI (presentation)
- SQLAlchemy 2.0 (async ORM)
- PostgreSQL
- AsyncIO
- structlog (structured logging)
- Ruff (linting)
- MyPy (static typing)
- Pytest (testing)

## 3. Architectural Principles

- Clean Architecture: strict separation between Domain, Application, Infrastructure and
  Presentation layers, with dependencies pointing inward.
- Domain-Driven Design: model core business concepts with entities, value objects, and domain
  errors; keep invariants inside the domain.
- SOLID + DI: single responsibility, explicit interfaces, and constructor injection to enable testing
  and composition.
- Repository Pattern & Unit of Work: repositories map between ORM and domain; Unit of Work
  encapsulates transaction boundaries (commit/rollback/close).
- CQRS-ready design: use cases are structured so commands and queries can be separated when
  warranted.

## 4. Layer Structure

- Domain
  - Contains entities, value objects, domain errors and domain services.
  - No external dependencies; represents the canonical business model.

- Application
  - Implements use cases (interactors), defines interfaces (ports) for persistence and external
    systems, and orchestrates domain operations.
  - Depends on Domain abstractions only; communicates with infrastructure via interfaces.

- Infrastructure
  - Implements repository ports, unit-of-work, database models, and external adapters.
  - Depends on Application and Domain ports; contains framework-specific code.

- Presentation
  - FastAPI routers, request/response schemas, authentication and authorization adapters.
  - Thin layer that validates and maps input, invokes use cases, and returns responses.

Allowed dependencies follow the inward rule: Presentation -> Application -> Domain. Infrastructure
implements the outbound ports consumed by Application.

## 5. Folder Structure

Core layout (existing repository):

- `backend/` — application package
  - `api/` — router composition and endpoints
  - `core/` — configuration, logging, database bootstrap
  - `modules/` — business modules (each a bounded context)
    - `<module>/domain/` — domain entities, value objects, exceptions
    - `<module>/application/` — use cases, ports, commands, services
    - `<module>/infrastructure/` — ORM models, repositories, adapters, unit-of-work
    - `<module>/presentation/` — FastAPI adapters and thin mapping code
  - `shared_kernel/` — small, stable primitives reused across modules

This structure matches the current repository layout; add new folders only when introducing a new
bounded context and after review.

## 6. Request Flow

1. HTTP request arrives at FastAPI endpoint (presentation).
2. Endpoint validates input, applies auth, and constructs a command/DTO.
3. Endpoint calls an Application use case (single responsibility) with injected ports.
4. Use case interacts with Repository interfaces and domain entities to perform work.
5. Repository implementations in Infrastructure map domain entities to ORM models and persist via
   AsyncSession.
6. Unit of Work controls transaction boundaries (commit/rollback) and closes the session.
7. Use case returns domain result; endpoint maps it to a response and returns to the client.

This flow mirrors the repository and unit-of-work implementations present under
`backend/modules/users/infrastructure`.

## 7. Dependency Rules

- Domain: no external dependencies.
- Application: may depend on Domain and application-level interfaces (ports).
- Presentation: depends on Application only.
- Infrastructure: depends on Application and Domain ports and contains concrete adapters.

Enforce these rules with code reviews and import checks; do not allow direct infrastructure imports
inside Application or Domain modules.

## 8. Database Rules

- ORM models live in `infrastructure.models` and are pure persistence representations (SQLAlchemy
  mapped columns, constraints, and indexes).
- Domain entities implement business invariants and are independent from ORM concerns.
- Repositories are the only place that map ORM instances to domain entities and vice versa. Keep
  this mapping explicit and well-tested.
- Unit of Work implementations (infrastructure) manage AsyncSession lifecycle and ensure commit,
  rollback and session close semantics.

## 9. Coding Standards

- Follow `.github/copilot-instructions.md` for automated code generation guidance.
- Target Ruff and MyPy: use modern typing (`Self`, `|` unions), avoid `Any` when possible.
- Keep functions small, prefer early returns, and limit line length to 100 characters.
- Tests: unit tests for Domain and Application; integration tests for Infrastructure; end-to-end for
  critical workflows.

## 10. Git Workflow

- Create a feature branch for each change.
- Make focused commits with clear messages and small diffs.
- Open a Pull Request that documents intent, design rationale and testing strategy.
- Ensure CI (linters, type checks, tests) passes before merge.

## 11. Future Architecture (Modules)

Future modules (examples) must follow the same pattern and be introduced as bounded contexts:

- Authentication, AI Agents, Memory, Notifications, Meetings, Analytics.

Each module must own its domain, application and infrastructure boundaries and reuse shared
interfaces from the `shared_kernel` where appropriate.

## 12. Non-negotiable Rules

- Never duplicate implementations.
- Never place business logic inside presentation endpoints.
- Never access SQLAlchemy from use cases or domain code.
- Never violate Clean Architecture dependency direction.
- Never commit placeholder code or TODOs.

---

Document maintained by the architecture team. Use this as the canonical onboarding and review
reference.
