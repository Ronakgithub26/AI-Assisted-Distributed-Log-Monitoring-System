import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..event_builder import build_event
from ..queue import EventQueue


class AgentFastAPIMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        try:
            response = await call_next(request)
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
                    "path": request.url.path,
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
                    "path": request.url.path,
                    "method": request.method,
                    "exception_type": type(e).__name__,
                    "message": str(e)
                }
            )

            EventQueue.push(event)

            raise


def init_fastapi(app):
    app.add_middleware(AgentFastAPIMiddleware)
