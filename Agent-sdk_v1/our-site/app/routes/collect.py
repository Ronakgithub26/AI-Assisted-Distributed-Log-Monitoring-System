from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from database import logs_collection
from schemas import CollectLogsRequest
from datetime import datetime
import csv
import os

router = APIRouter()

CSV_FILE = "logs.csv"

@router.post("/logs/collect", summary="Collect Logs")
async def collect_logs(payload):
    print(payload)
    inserted_count = 0
    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write header first time
            if not file_exists:
                writer.writerow(["timestamp", "api_key", "type", "message", "payload"])

            for event in payload.events:

                log_data = {
                    "timestamp": datetime.utcnow(),
                    "api_key": payload.api_key,
                    "type": event.type,
                    "message": event.message,
                    "payload": event.payload
                }

                # ✅ 1️⃣ Save to MongoDB
                logs_collection.insert_one(log_data)

                # ✅ 2️⃣ Save to CSV
                writer.writerow([
                    log_data["timestamp"],
                    log_data["api_key"],
                    log_data["type"],
                    log_data["message"],
                    str(log_data["payload"])
                ])

                inserted_count += 1

        return {
            "status": "ok",
            "ingested": inserted_count,
            "storage": ["mongodb", "csv"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs/view", response_class=HTMLResponse)
async def view_logs():

    logs = list(logs_collection.find().sort("timestamp", -1).limit(50))

    rows = ""
    for log in logs:
        rows += f"""
        <tr>
            <td>{log.get('timestamp')}</td>
            <td>{log.get('api_key')}</td>
            <td>{log.get('type')}</td>
            <td>{log.get('message')}</td>
        </tr>
        """

    html_content = f"""
    <html>
    <head>
        <title>Monitoring Dashboard</title>
        <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    </head>
    <body class="bg-dark text-white">
        <div class="container mt-4">
            <h2 class="text-warning text-center">📊 Monitoring Dashboard</h2>
            <div class="card mt-4 p-3">
                <table class="table table-striped table-bordered">
                    <thead class="table-dark">
                        <tr>
                            <th>Timestamp</th>
                            <th>API Key</th>
                            <th>Type</th>
                            <th>Message</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    return html_content

