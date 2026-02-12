import time
from ..event_builder import build_event
from ..queue import EventQueue


class AgentDjangoMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        try:
            response = self.get_response(request)
            duration_ms = int((time.time() - start_time) * 1000)

            status_code = response.status_code

            # Classification
            if status_code >= 500:
                event_type = "SERVER_ERROR"
                status = "FAILURE"
            elif status_code >= 400:
                event_type = "ROUTING_ERROR"
                status = "FAILURE"
            else:
                event_type = "INCOMING_REQUEST"
                status = "SUCCESS"

            event = build_event(
                event_type=event_type,
                category="APPLICATION",
                status=status,
                metrics={
                    "duration_ms": duration_ms
                },
                data={
                    "path": request.path,
                    "method": request.method,
                    "status_code": status_code
                }
            )

            EventQueue.push(event)

            return response

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)

            event = build_event(
                event_type="SERVER_ERROR",
                category="APPLICATION",
                status="FAILURE",
                metrics={
                    "duration_ms": duration_ms
                },
                data={
                    "path": request.path,
                    "method": request.method,
                    "exception_type": type(e).__name__,
                    "message": str(e)
                }
            )

            EventQueue.push(event)

            raise
