import sys
import traceback
import threading
from .event_builder import build_event
from .queue import EventQueue


class ExceptionTracker:

    @staticmethod
    def install():
        sys.excepthook = ExceptionTracker.handle_exception

        # Python 3.8+ thread exception support
        if hasattr(threading, "excepthook"):
            threading.excepthook = ExceptionTracker.handle_thread_exception

    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        try:
            ExceptionTracker._process_exception(
                exc_type,
                exc_value,
                exc_traceback,
                handled=False
            )
        except Exception:
            pass  # Never crash app

    @staticmethod
    def handle_thread_exception(args):
        try:
            ExceptionTracker._process_exception(
                args.exc_type,
                args.exc_value,
                args.exc_traceback,
                handled=False
            )
        except Exception:
            pass

    @staticmethod
    def _process_exception(exc_type, exc_value, exc_traceback, handled):

        stack = "".join(
            traceback.format_exception(exc_type, exc_value, exc_traceback)
        )

        last_trace = traceback.extract_tb(exc_traceback)[-1] if exc_traceback else None

        file_name = last_trace.filename if last_trace else None
        line_number = last_trace.lineno if last_trace else None
        function_name = last_trace.name if last_trace else None

        payload = {
            "error_type": exc_type.__name__,
            "message": str(exc_value),
            "file": file_name,
            "line": line_number,
            "function": function_name,
            "stacktrace": stack,
            "handled": handled
        }

        event = build_event(
            event_type="EXCEPTION",
            category="APPLICATION",
            status="FAILURE",
            data=payload,
            metrics={}
        )

        EventQueue.push(event)
