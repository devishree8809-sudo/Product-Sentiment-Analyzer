"""
import_reviews.py
------------------
Reads reviews.csv (from the Web Scraping Team) and loads it into:
  - Products collection
  - Reviews collection

Usage:
    python import_reviews.py
"""

import os
import sys
import pandas as pd

db_dir = os.path.dirname(os.path.abspath(__file__))
if db_dir not in sys.path:
    sys.path.insert(0, db_dir)

from mongodb_connection import get_db, test_connection

CSV_PATH = os.path.join(os.path.dirname(__file__), "reviews.csv")

def import_reviews():
    if not test_connection():
        return

    db = get_db()

    products_collection = db["Products"]
    reviews_collection = db["Reviews"]

    if not os.path.exists(CSV_PATH):
        print(f"\nERROR: CSV file not found:\n{CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)

    df["Product Name"] = df["Product Name"].astype(str).str.strip()
    df["Review Text"] = df["Review Text"].astype(str).str.strip()

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
        }
    )

    unique_products = df["productName"].unique()

    for product in unique_products:
        products_collection.update_one(
            {"productName": product},
            {"$setOnInsert": {"productName": product}},
            upsert=True,
        )

    inserted = 0

    for _, row in df.iterrows():
        doc = row.to_dict()

        exists = reviews_collection.find_one(
            {
                "productName": doc["productName"],
                "review": doc["review"],
                "reviewerName": doc["reviewerName"],
                "reviewDate": doc["reviewDate"],
            }
        )

        if not exists:
            reviews_collection.insert_one(doc)
            inserted += 1

    print("\nImport Complete")
    print("----------------")
    print("Products :", len(unique_products))
    print("Inserted :", inserted)
    print("Total Reviews :", reviews_collection.count_documents({}))

if __name__ == "__main__":
    import_reviews()
