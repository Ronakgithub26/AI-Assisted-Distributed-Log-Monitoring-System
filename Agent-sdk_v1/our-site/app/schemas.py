from pydantic import BaseModel
from typing import List, Dict, Any

class LogEvent(BaseModel):
    type: str
    message: str | None = None
    payload: Dict[str, Any] | None = None

class CollectLogsRequest(BaseModel):
    api_key: str
    events: List[LogEvent]
