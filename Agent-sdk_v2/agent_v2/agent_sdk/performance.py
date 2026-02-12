import time
from functools import wraps
from .event_builder import build_event
from .queue import EventQueue


DEFAULT_SLOW_THRESHOLD_MS = 500


def monitor_performance(threshold_ms=DEFAULT_SLOW_THRESHOLD_MS):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration_ms = int((time.time() - start) * 1000)

                if duration_ms >= threshold_ms:
                    event_type = "SLOW_FUNCTION"
                    status = "WARNING"
                else:
                    event_type = "FUNCTION_CALL"
                    status = "SUCCESS"

                event = build_event(
                    event_type=event_type,
                    category="APPLICATION",
                    status=status,
                    metrics={
                        "duration_ms": duration_ms
                    },
                    data={
                        "function_name": func.__name__,
                        "module": func.__module__
                    }
                )

                EventQueue.push(event)

        return wrapper

    return decorator
