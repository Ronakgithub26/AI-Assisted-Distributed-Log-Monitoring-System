import logging
import traceback
from .event_builder import build_event
from .queue import EventQueue


LOG_LEVEL_SEVERITY = {
    logging.DEBUG: "LOW",
    logging.INFO: "LOW",
    logging.WARNING: "MEDIUM",
    logging.ERROR: "HIGH",
    logging.CRITICAL: "CRITICAL",
}


class AgentLogHandler(logging.Handler):

    def emit(self, record):

        try:
            severity = LOG_LEVEL_SEVERITY.get(record.levelno, "LOW")

            stacktrace = None
            if record.exc_info:
                stacktrace = "".join(
                    traceback.format_exception(*record.exc_info)
                )

            event = build_event(
                event_type="LOG",
                category="APPLICATION",
                status="FAILURE" if record.levelno >= logging.ERROR else "SUCCESS",
                metrics={},
                data={
                    "logger_name": record.name,
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "file": record.pathname,
                    "line": record.lineno,
                    "stacktrace": stacktrace
                }
            )

            # Override severity manually
            event["event"]["severity"] = severity

            EventQueue.push(event)

        except Exception:
            pass


def install_logging(level=logging.WARNING):
    handler = AgentLogHandler()
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(level)
