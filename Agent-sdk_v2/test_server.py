from fastapi import FastAPI, Header, HTTPException, Request
import hmac
import hashlib
import json
from datetime import datetime, timezone

app = FastAPI()

# For testing only
API_KEYS = {
    "demo-key": "super-secret"
}

# Temporary memory storage
EVENT_STORE = []


def verify_signature(api_key, timestamp, signature, body):

    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    secret = API_KEYS[api_key]

    message = timestamp + body

    expected_signature = hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Optional: timestamp freshness check (5 min window)
    try:
        ts = datetime.fromisoformat(timestamp)
        now = datetime.now(timezone.utc)
        if abs((now - ts).total_seconds()) > 300:
            raise HTTPException(status_code=401, detail="Timestamp expired")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timestamp")


@app.post("/api/logs")
async def receive_logs(
    request: Request,
    x_api_key: str = Header(...),
    x_timestamp: str = Header(...),
    x_signature: str = Header(...)
):

    body_bytes = await request.body()
    body_str = body_bytes.decode()

    # verify_signature(
    #     x_api_key,
    #     x_timestamp,
    #     x_signature,
    #     body_str
    # )

    payload = json.loads(body_str)

    print("\n📦 Received Batch")
    print("Event Count:", payload["batch_meta"]["event_count"])

    for event in payload["events"]:
        print("→", event["event"]["type"])
        print(event)

    EVENT_STORE.append(payload)

    return {"status": "received"}
