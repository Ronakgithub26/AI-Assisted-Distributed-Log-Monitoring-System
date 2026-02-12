def normalize_event(event: dict):
    return {
        "type": event.get("type", "UNKNOWN"),
        "message": event.get("message", ""),
        "payload": event
    }
