Project: Athena AI

Purpose
- Provide concise, authoritative guidance to GitHub Copilot for generating code that fits Athena AI's production standards.

Tech stack
- Python 3.13
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- AsyncIO
- Clean Architecture
- Domain-Driven Design

Core rules (must follow)
- Never create duplicate classes or duplicate file contents.
- Never mix multiple implementations in a single file; one responsibility per file.
- Do not invent imports — reuse existing interfaces or add imports only when they exist in the repository.
- Reuse existing domain and application interfaces; prefer depending on abstractions, not concrete implementations.
- Follow SOLID, DRY, KISS and prefer composition over inheritance.
- Use dependency injection for wiring dependencies.
- Implement async APIs using `async`/`await` where IO or concurrency is involved.
- Target Ruff and MyPy compatibility: write statically-typed code with modern typing (`Self`, `|` unions, parameter/return annotations).
- Keep code idiomatic for Python 3.13 and avoid legacy patterns.
- Do not create DTOs unless explicitly requested by the task description.
- Do not change business logic unless the user explicitly asks for it.

Architecture & design
- Follow Clean Architecture and DDD boundaries: domain (entities, value objects, domain errors) → application (use cases, interfaces) → infrastructure (persistence, external adapters) → presentation (API endpoints).
- Application code should depend on interfaces defined in `application.interfaces` or domain repository interfaces, not on infrastructure modules.
- Domain objects must contain domain rules and validation; application services orchestrate use cases.

Typing & quality
- Use `typing.Self` and `types.TracebackType` where appropriate.
- Prefer explicit types over `Any`; keep mypy happy.
- Avoid forward-string annotations when runtime names are available; prefer real names.
- Keep functions small and single-purpose; favor private helpers for decomposition.

Database & persistence
- Use SQLAlchemy 2.0 AsyncSession in infrastructure code; repository implementations translate between ORM models and domain entities.
- Do not place SQLAlchemy models in domain or application layers.

Security & secrets
- Never commit secrets or credentials. Use environment configuration only.

Testing & reliability
- Prefer small, focused unit tests for domain and application code; integration tests for infrastructure.
- Make resources exception-safe (use `try/finally` or context managers) and do not swallow exceptions silently.

Commit & PR guidance
- Keep changes small and focused. Explain intent in PR description.
- Include tests for new behavior and update type hints accordingly.

When in doubt
- Ask a clarifying question before making design-altering changes.
- If a requested implementation requires new interfaces, propose them in the PR and get approval.

Stop: create only the files explicitly requested by the user and no additional artifacts.

## Imports
- Use absolute imports only.
- Never use wildcard imports.
- Keep imports grouped and sorted.
- Avoid circular imports whenever possible.

## Existing Code
- Always inspect the existing file before generating code.
- Never overwrite existing implementations.
- Extend existing implementations instead of replacing them.
- Never generate duplicate classes or duplicate file contents.

## File Creation
- Never create new files unless explicitly requested.
- Never rename existing files.
- Never move files.
- Never modify unrelated files.

## Repository Pattern
- Repositories translate only between ORM models and domain entities.
- Repositories must not contain business logic.
- Business logic belongs to the domain layer.

## Application Layer
- Use cases must have a single responsibility.
- Use cases orchestrate domain objects.
- Use cases must never access SQLAlchemy directly.

## Presentation Layer
- FastAPI endpoints must remain thin.
- Endpoints validate input, call use cases, and return responses.
- Never place business logic inside API endpoints.

## Logging
- Never use print().
- Use structlog for logging.

## Exceptions
- Never silently ignore exceptions.
- Never catch Exception unless preserving or re-raising the original exception.

## Code Style
- Maximum line length: 100 characters.
- Prefer early returns.
- Avoid deep nesting.
- Keep functions small and focused.

## AI Assistant Workflow

Before generating code:

1. Inspect the existing implementation.
2. Preserve the existing architecture.
3. Generate only the requested file.
4. Stop immediately after finishing the requested task.
5. Never generate TODO placeholders.
6. Never assume missing interfaces.
7. Ask for clarification if architecture is unclear.

Do not modify the existing project architecture.

Only improve this file.
