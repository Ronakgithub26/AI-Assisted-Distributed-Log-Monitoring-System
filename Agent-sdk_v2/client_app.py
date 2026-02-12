from flask import Flask, render_template_string
from agent_sdk import Agent
from agent_sdk.performance import monitor_performance
import requests
import logging
import time
from sqlalchemy import create_engine, text

app = Flask(__name__)

# ----------------------------
# Database (SQLite for testing)
# ----------------------------
engine = create_engine("sqlite:///test.db")

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"))
    conn.commit()

# ----------------------------
# Initialize Agent
# ----------------------------
Agent.init(
    api_key="demo-key",
    api_secret="super-secret",
    endpoint="http://127.0.0.1:8000/api/logs",
    project="client-test-app",
    framework="flask",
    app=app,
    db_engine=engine,
    enable_http=True,
    enable_logging=True,
    enable_exceptions=True,
    enable_performance=True
)

# ----------------------------
# Dashboard UI
# ----------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Agent SDK Test Dashboard</title>
    <style>
        body {
            font-family: Arial;
            background: #111;
            color: #eee;
            text-align: center;
        }
        h1 { color: #00ffcc; }
        button {
            margin: 10px;
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
        .btn { background: #00ffcc; }
        .danger { background: #ff4d4d; }
        .warn { background: #ffaa00; }
        .info { background: #3399ff; }
        #result {
            margin-top: 20px;
            padding: 10px;
            background: #222;
            border-radius: 8px;
        }
    </style>
</head>
<body>

<h1>🚀 Agent SDK Test Dashboard</h1>

<button class="btn" onclick="hit('/external')">HTTP Success</button>
<button class="warn" onclick="hit('/http-error')">HTTP Error (404)</button>
<button class="danger" onclick="hit('/crash')">Trigger Exception</button>
<button class="info" onclick="hit('/log-error')">Log Error</button>
<button class="warn" onclick="hit('/slow')">Slow Function</button>
<button class="btn" onclick="hit('/db')">DB Insert</button>
<button class="danger" onclick="hit('/db-error')">DB Error</button>

<div id="result">Click a button to trigger event...</div>

<script>
async function hit(route) {
    document.getElementById("result").innerText = "Calling " + route + "...";

    try {
        const res = await fetch(route);
        const text = await res.text();
        document.getElementById("result").innerText = text;
    } catch (e) {
        document.getElementById("result").innerText = "Error: " + e;
    }
}
</script>

</body>
</html>
"""

@app.route("/")
def dashboard():
    return render_template_string(HTML_PAGE)

# ----------------------------
# Event Routes
# ----------------------------

@app.route("/external")
def external_call():
    requests.get("https://httpbin.org/get")
    return "✅ External HTTP Success"

@app.route("/http-error")
def http_error():
    requests.get("https://httpbin.org/status/404")
    return "⚠ HTTP 404 Triggered"

@app.route("/crash")
def crash():
    return 1 / 0

@app.route("/log-error")
def log_error():
    logging.error("This is a test error log")
    return "📝 Logged error"

@monitor_performance(threshold_ms=300)
def slow_function():
    time.sleep(1)

@app.route("/slow")
def slow():
    slow_function()
    return "🐢 Slow function executed"

@app.route("/db")
def db_test():
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO users (name) VALUES ('John')"))
        conn.commit()
    return "🗄 DB Insert Done"

@app.route("/db-error")
def db_error():
    with engine.connect() as conn:
        conn.execute(text("INSERT INTO invalid_table VALUES (1)"))
        conn.commit()
    return "Should fail"

# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    app.run(port=5000)
