"""
mongodb_connection.py
----------------------
Single shared MongoDB connection.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import traceback

_current_dir = os.path.dirname(os.path.abspath(__file__))
_backend_env = os.path.abspath(os.path.join(_current_dir, "..", "backend", ".env"))
if os.path.exists(_backend_env):
    load_dotenv(_backend_env)
else:
    load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DATABASE_NAME", "ProductSentimentDB")

_client = None

def get_client():
    global _client

    if _client is None:
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

    return _client

def get_db():
    return get_client()[DB_NAME]

def test_connection():
    try:
        client = get_client()

        client.admin.command("ping")

        print("=" * 60)
        print("MongoDB Connected Successfully")
        print(f"Mongo URI : {MONGO_URI}")
        print(f"Database  : {DB_NAME}")
        print("=" * 60)

        return True

    except Exception as e:
        print("=" * 60)
        print("MongoDB Connection FAILED")
        print("=" * 60)

        traceback.print_exc()

        print("\nException:")
        print(e)

        print("=" * 60)

        return False

if __name__ == "__main__":
    test_connection()
