import os
import json
import datetime
from logging.handlers import RotatingFileHandler
import logging
from flask import Flask, request
from generator import DecoyGenerator
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = os.getenv("HP_LOG_PATH", "logs/honeypot.json")
GEN_MODE = os.getenv("HP_GENERATOR", "template")
os.makedirs(os.path.dirname(LOG_PATH) or ".", exist_ok=True)

handler = RotatingFileHandler(LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=5)
handler.setFormatter(logging.Formatter("%(message)s"))
logger = logging.getLogger("honeypot")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

app = Flask(__name__)
gen = DecoyGenerator(mode=GEN_MODE)

def get_client_ip():
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr

def log_event(event):
    logger.info(json.dumps(event, ensure_ascii=False))

def make_event():
    return {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "path": request.path,
        "method": request.method,
        "ip": get_client_ip(),
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "body": request.get_data(as_text=True),
    }

@app.route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/admin", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/api/login", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/.env", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def trap():
    ev = make_event()
    ev["suspicious"] = any(word in ev["body"].lower() for word in ["password", "passwd"])
    log_event(ev)
    resp_text = gen.generate_response(ev)
    return resp_text, 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    print(f"Starting honeypot (generator mode={GEN_MODE}). Logging to {LOG_PATH}")
    app.run(host="0.0.0.0", port=5000, debug=False)
