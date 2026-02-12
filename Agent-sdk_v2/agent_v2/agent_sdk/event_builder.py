import uuid
from datetime import datetime, timezone
from .config import AgentConfig
from .identity import Identity
from .severity import get_severity


def current_utc():
    return datetime.now(timezone.utc).isoformat()


def build_event(event_type, category, status, data, metrics=None):

    return {
        "meta": {
            "sdk_version": AgentConfig.sdk_version,
            "schema_version": AgentConfig.schema_version,
            "timestamp": current_utc(),
            "trace_id": str(uuid.uuid4()),
            "project": AgentConfig.project,
            "environment": AgentConfig.environment
        },

        "identity": Identity.collect(
            api_key=AgentConfig.api_key
        ),

        "event": {
            "category": category,
            "type": event_type,
            "severity": get_severity(event_type),
            "status": status,
            "metrics": metrics or {},
            "data": data
        }
    }

