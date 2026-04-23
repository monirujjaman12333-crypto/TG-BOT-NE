import subprocess
import threading
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

# ✅ Render এ /tmp তে data রাখো (writable)
os.environ.setdefault("DATA_DIR", "/tmp/data")
os.makedirs("/tmp/data", exist_ok=True)

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"OK")
        self.wfile.flush()
    def log_message(self, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(("0.0.0.0", port), HealthHandler).serve_forever()

# Health check server চালু রাখো
threading.Thread(target=run_server, daemon=True).start()

def run_with_restart(name, cmd):
    """Process crash হলে auto restart করবে"""
    while True:
        print(f"▶️ Starting {name}...")
        try:
            proc = subprocess.Popen(cmd)
            proc.wait()
            print(f"⚠️ {name} stopped! Restarting in 5 seconds...")
        except Exception as e:
            print(f"❌ {name} error: {e}")
        time.sleep(5)

# bot.py আলাদা thread এ চালাও
t1 = threading.Thread(
    target=run_with_restart,
    args=("bot.py", ["python", "bot.py"]),
    daemon=True
)
t1.start()

# ⚠️ bot.py এর ভেতরেই otp_monitor thread আছে
# তাই আলাদা করে চালাতে হবে না

# Main thread জীবিত রাখো
while True:
    time.sleep(60)
    print("✅ Main process alive...")
