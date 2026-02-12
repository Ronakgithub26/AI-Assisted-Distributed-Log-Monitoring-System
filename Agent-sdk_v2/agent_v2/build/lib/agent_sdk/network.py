import time
import requests
from urllib.parse import urlparse
from .event_builder import build_event
from .queue import EventQueue
from .config import AgentConfig


_original_request = None


def install_http_patch():
    global _original_request

    if _original_request is not None:
        return  # Already patched

    _original_request = requests.Session.request

    def patched_request(self, method, url, **kwargs):

        # 🔥 Ignore SDK internal endpoint
        if AgentConfig.endpoint:
            try:
                if urlparse(url).netloc == urlparse(AgentConfig.endpoint).netloc:
                    return _original_request(self, method, url, **kwargs)
            except Exception:
                pass

        start = time.time()

        try:
            response = _original_request(self, method, url, **kwargs)
            duration_ms = int((time.time() - start) * 1000)

            # ----------------------------
            # HTTP 4xx / 5xx Handling
            # ----------------------------
            if response.status_code >= 400:

                event = build_event(
                    event_type="HTTP_ERROR",
                    category="NETWORK",
                    status="FAILURE",
                    metrics={
                        "duration_ms": duration_ms
                    },
                    data={
                        "method": method,
                        "url": url,
                        "status_code": response.status_code,
                        "response_size": len(response.content)
                    }
                )

                EventQueue.push(event)

            else:
                # Successful call
                event = build_event(
                    event_type="HTTP_CALL",
                    category="NETWORK",
                    status="SUCCESS",
                    metrics={
                        "duration_ms": duration_ms
                    },
                    data={
                        "method": method,
                        "url": url,
                        "status_code": response.status_code
                    }
                )

                EventQueue.push(event)

            return response

        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)

            event = build_event(
                event_type="HTTP_EXCEPTION",
                category="NETWORK",
                status="FAILURE",
                metrics={
                    "duration_ms": duration_ms
                },
                data={
                    "method": method,
                    "url": url,
                    "exception_type": type(e).__name__,
                    "message": str(e)
                }
            )

            EventQueue.push(event)

            raise

    requests.Session.request = patched_request
