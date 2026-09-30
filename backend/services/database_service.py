import sys
import os

DATABASE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "database")
)

if DATABASE_PATH not in sys.path:
    sys.path.append(DATABASE_PATH)

from mongodb_connection import get_db, test_connection

def connect_database():
    return test_connection()

def database():
    return get_db()
