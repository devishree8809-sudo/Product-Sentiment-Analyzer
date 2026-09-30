"""
database.py
------------
Main entry point. Run this one file to build the whole database:
  1. Connect to MongoDB
  2. Import reviews.csv -> Products + Reviews collections
  3. Import sentiment_results.csv -> SentimentResults collection

Usage:
  python database.py
"""

import os
import sys

db_dir = os.path.dirname(os.path.abspath(__file__))
if db_dir not in sys.path:
    sys.path.insert(0, db_dir)

from mongodb_connection import test_connection
from import_reviews import import_reviews
from import_sentiment import import_sentiment

if __name__ == "__main__":
    print("=== Step 1: Testing MongoDB connection ===")
    if not test_connection():
        print("Fix your connection (check mongodb_connection.py) before continuing.")
        exit(1)

    print("\n=== Step 2: Importing reviews.csv ===")
    import_reviews()

    print("\n=== Step 3: Importing sentiment_results.csv ===")
    import_sentiment()

    print("\nDatabase build complete.")
