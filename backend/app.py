import os
import sys

backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from flask import Flask, jsonify
from flask_cors import CORS

from routes.health import health_bp
from routes.analyze import analyze_bp

from services.database_service import connect_database

app = Flask(__name__)

CORS(app)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "running",
        "backend": "Flask",
        "message": "Use /health for server status, or /analyze/<product_name> for sentiment analysis."
    })

app.register_blueprint(health_bp)
app.register_blueprint(analyze_bp)

print("=" * 60)
print("Python Executable:")
print(sys.executable)
print("=" * 60)

print("Connecting to MongoDB...")

if connect_database():
    print("MongoDB Connected Successfully")
else:
    print("MongoDB Connection Failed")

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
