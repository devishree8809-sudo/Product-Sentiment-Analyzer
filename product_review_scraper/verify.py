"""
Verification script: Tests all scraper components and generates
a reviews.csv sample without making any live network requests.
"""
import sys
import os
import pandas as pd

results = []

def run_test(name, fn):
    try:
        fn()
        results.append(f"  PASS  {name}")
    except AssertionError as e:
        results.append(f"  FAIL  {name} -> {e}")
    except Exception as e:
        results.append(f"  ERROR {name} -> {e}")

from scrapers.amazon import AmazonScraper
from scrapers.flipkart import FlipkartScraper

def test_headers():
    s = AmazonScraper()
    h = s.get_headers()
    assert "User-Agent" in h
    assert h["User-Agent"].startswith("Mozilla/5.0")
    assert "Accept" in h

run_test("BaseScraper: Header rotation produces valid browser headers", test_headers)

def test_amazon_known():
    s = AmazonScraper()
    reviews = s._generate_mock_reviews("B0BY8MCQ9S", 10)
    assert len(reviews) == 10
    for r in reviews:
        assert "Product Name" in r
        assert "Review Text" in r
        assert "Rating" in r
        assert 1.0 <= r["Rating"] <= 5.0
        assert r["Product Name"] == "Apple iPhone 14 (128 GB) - Blue"

run_test("AmazonScraper: Mock generator for known ASIN (B0BY8MCQ9S)", test_amazon_known)

def test_amazon_unknown():
    s = AmazonScraper()
    reviews = s._generate_mock_reviews("B000UNKNOWN", 5)
    assert len(reviews) == 5
    assert reviews[0]["Product Name"] == "Amazon Product (ASIN: B000UNKNOWN)"

run_test("AmazonScraper: Mock generator for unknown ASIN (generic fallback)", test_amazon_unknown)

def test_flipkart_known():
    s = FlipkartScraper()
    reviews = s._generate_mock_reviews("apple-iphone-15", "MOBGTAGPAHB5E8AS", 8)
    assert len(reviews) == 8
    for r in reviews:
        assert r["Product Name"] == "Apple iPhone 15 (Black, 128 GB)"
        assert 1.0 <= r["Rating"] <= 5.0

run_test("FlipkartScraper: Mock generator for known product ID (MOBGTAGPAHB5E8AS)", test_flipkart_known)

def test_flipkart_unknown():
    s = FlipkartScraper()
    reviews = s._generate_mock_reviews("some-gadget", "MOB99999", 5)
    assert len(reviews) == 5
    assert reviews[0]["Product Name"] == "Some Gadget (ID: MOB99999)"

run_test("FlipkartScraper: Mock generator for unknown product (generic fallback)", test_flipkart_unknown)

def test_schema():
    s = AmazonScraper()
    reviews = s._generate_mock_reviews("B0BY8MCQ9S", 5)
    df = pd.DataFrame(reviews)
    required = ["Product Name", "Review Text", "Rating", "Review Date", "Reviewer Name"]
    for col in required:
        assert col in df.columns, f"Missing column: {col}"
    assert len(df) == 5

run_test("DataFrame: Schema has all 5 required columns", test_schema)

passed = sum(1 for r in results if r.strip().startswith("PASS"))
failed = sum(1 for r in results if r.strip().startswith("FAIL") or r.strip().startswith("ERROR"))

print("=" * 60)
print("              UNIT TEST RESULTS                ")
print("=" * 60)
for r in results:
    print(r)
print("-" * 60)
print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
print("=" * 60)

amazon = AmazonScraper()
flipkart = FlipkartScraper()

amazon_reviews  = amazon._generate_mock_reviews("B0BY8MCQ9S", 10)
amazon_reviews2 = amazon._generate_mock_reviews("B07ZPKN856", 10)
fk_reviews      = flipkart._generate_mock_reviews("apple-iphone-15", "MOBGTAGPAHB5E8AS", 10)
fk_reviews2     = flipkart._generate_mock_reviews("motorola-g34-5g", "MOBGUZNEH78GG3HW", 10)

all_reviews = amazon_reviews + amazon_reviews2 + fk_reviews + fk_reviews2

df = pd.DataFrame(all_reviews)
df = df[["Product Name", "Review Text", "Rating", "Review Date", "Reviewer Name"]]

output_path = os.path.join(os.path.dirname(__file__), "reviews.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\nreviews.csv generated successfully!")
print(f"Total reviews written : {len(df)}")
print(f"Products included      : {df['Product Name'].nunique()}")
print(f"\nProduct breakdown:")
for product, count in df.groupby("Product Name").size().items():
    print(f"  - {product}: {count} reviews")
print(f"\nSample rows:")
print(df.head(3).to_string(index=False))
print("=" * 60)
