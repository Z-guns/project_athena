import logging
import sys
from collections.abc import Iterable

import structlog
from structlog.typing import Processor


def _shared_processors() -> list[Processor]:
    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.ExceptionRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]


def _renderer(*, json_logs: bool) -> Processor:
    if json_logs:
        return structlog.processors.JSONRenderer()
    return structlog.dev.ConsoleRenderer(colors=sys.stderr.isatty())


def configure_logging(
    *,
    log_level: str = "INFO",
    environment: str = "development",
    json_logs: bool | None = None,
    noisy_loggers: Iterable[str] = ("uvicorn.access",),
) -> None:
    """Configure structlog and standard-library logging for the application."""
    level = logging.getLevelNamesMapping().get(log_level.upper())
    if level is None:
        raise ValueError(f"Unknown log level: {log_level!r}")

    use_json = environment.lower() == "production" if json_logs is None else json_logs
    shared_processors = _shared_processors()

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            _renderer(json_logs=use_json),
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)

    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
