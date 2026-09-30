#!/usr/bin/env python
"""
Product Review Scraper CLI
Extracts reviews from Amazon or Flipkart and exports them to a structured CSV.
"""

import os
import argparse
import pandas as pd
from scrapers.amazon import AmazonScraper
from scrapers.flipkart import FlipkartScraper

def main():
    parser = argparse.ArgumentParser(
        description="Scrape reviews from Amazon or Flipkart and save them to a CSV file."
    )

    parser.add_argument(
        "--source",
        choices=["amazon", "flipkart"],
        required=True,
        help="Select the e-commerce source to scrape reviews from."
    )

    parser.add_argument(
        "--target",
        required=True,
        help="The scrape target (ASIN for Amazon, product slug for Flipkart)."
    )

    parser.add_argument(
        "--id",
        dest="product_id",
        default="",
        help="Flipkart product ID (required for live Flipkart scraping, starts with MOB...)."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of reviews to extract (default: 50)."
    )

    parser.add_argument(
        "--output",
        default="reviews.csv",
        help="Path to the output CSV file (default: reviews.csv)."
    )

    parser.add_argument(
        "--domain",
        default="in",
        help="Country domain code for Amazon. e.g., 'in' for amazon.in, 'com' for amazon.com (default: in)."
    )

    args = parser.parse_args()

    print("=" * 60)
    print("             PRODUCT REVIEW WEB SCRAPER             ")
    print("=" * 60)
    print(f"Source:      {args.source.upper()}")
    print(f"Target:      {args.target}")
    if args.source == "flipkart" and args.product_id:
        print(f"Product ID:  {args.product_id}")
    if args.source == "amazon":
        print(f"Amazon TLD:  amazon.{args.domain}")
    print(f"Limit:       {args.limit} reviews")
    print(f"Output File: {args.output}")
    print("-" * 60)

    if args.source == "amazon":
        scraper = AmazonScraper()
        kwargs = {"domain": args.domain}
    else:
        scraper = FlipkartScraper()
        kwargs = {"product_id": args.product_id}

    try:
        reviews_data = scraper.scrape(args.target, limit=args.limit, **kwargs)

        if not reviews_data:
            print("[ERROR] No reviews were collected. Exiting.")
            return

        df = pd.DataFrame(reviews_data)

        required_cols = ["Product Name", "Review Text", "Rating", "Review Date", "Reviewer Name"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""

        df = df[required_cols]

        output_dir = os.path.dirname(os.path.abspath(args.output))
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        df.to_csv(args.output, index=False, encoding="utf-8-sig")

        print("\n" + "=" * 60)
        print("                   SCRAPING SUMMARY                   ")
        print("=" * 60)
        print(f"Product Name:    {df['Product Name'].iloc[0]}")
        print(f"Total Extracted: {len(df)} reviews")
        print(f"Average Rating:  {df['Rating'].mean():.2f} / 5.0")

        print("\nRating Distribution:")
        rating_counts = df['Rating'].value_counts().sort_index(ascending=False)
        for rating, count in rating_counts.items():
            percentage = (count / len(df)) * 100
            bar = "★" * int(rating) + "☆" * (5 - int(rating))
            print(f"  {rating:.1f} Star {bar} | {count:3d} ({percentage:5.1f}%)")

        print("\nSample Review Preview:")
        preview_review = df.iloc[0]
        print(f"  Reviewer: {preview_review['Reviewer Name']}")
        print(f"  Date:     {preview_review['Review Date']}")
        print(f"  Rating:   {preview_review['Rating']} / 5.0")
        text_preview = preview_review['Review Text']
        if len(text_preview) > 100:
            text_preview = text_preview[:97] + "..."
        print(f"  Text:     \"{text_preview}\"")
        print("=" * 60)
        print(f"[SUCCESS] Data exported successfully to: {args.output}\n")

    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to execute scraping script: {e}")

if __name__ == "__main__":
    main()
