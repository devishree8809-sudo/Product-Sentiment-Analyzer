"""
import_sentiment.py
--------------------
Reads sentiment_results.csv and loads it into SentimentResults.

Usage:
    python import_sentiment.py
"""

import os
import sys
import pandas as pd

db_dir = os.path.dirname(os.path.abspath(__file__))
if db_dir not in sys.path:
    sys.path.insert(0, db_dir)

from mongodb_connection import get_db, test_connection

CSV_PATH = os.path.join(os.path.dirname(__file__), "sentiment_results.csv")

def import_sentiment():
    if not test_connection():
        return

    db = get_db()

    sentiment_collection = db["SentimentResults"]

    if not os.path.exists(CSV_PATH):
        print(f"\nERROR: CSV file not found:\n{CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)

    df["Product Name"] = df["Product Name"].astype(str).str.strip()
    df["Review Text"] = df["Review Text"].astype(str).str.strip()
    df["Sentiment"] = (
        df["Sentiment"]
        .astype(str)
        .str.strip()
        .str.capitalize()
    )

    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "Product Name",
            "Review Text",
            "Reviewer Name",
            "Review Date",
        ]
    )

    print(f"Removed {before-len(df)} duplicate rows.")

    df = df.rename(
        columns={
            "Product Name": "productName",
            "Review Text": "review",
            "Rating": "rating",
            "Review Date": "reviewDate",
            "Reviewer Name": "reviewerName",
            "Sentiment": "sentiment",
        }
    )

    inserted = 0
    updated = 0

    for _, row in df.iterrows():
        doc = row.to_dict()

        result = sentiment_collection.update_one(
            {
                "productName": doc["productName"],
                "review": doc["review"],
                "reviewerName": doc["reviewerName"],
                "reviewDate": doc["reviewDate"],
            },
            {"$set": doc},
            upsert=True,
        )

        if result.upserted_id:
            inserted += 1
        elif result.modified_count:
            updated += 1

    print("\nImport Complete")
    print("----------------")
    print("Inserted :", inserted)
    print("Updated :", updated)
    print("Total Sentiments :", sentiment_collection.count_documents({}))

if __name__ == "__main__":
    import_sentiment()
