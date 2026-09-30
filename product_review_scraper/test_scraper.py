import unittest
import pandas as pd
from scrapers.base import BaseScraper
from scrapers.amazon import AmazonScraper
from scrapers.flipkart import FlipkartScraper

class TestScrapers(unittest.TestCase):

    def test_base_scraper_headers(self):
        """Test that BaseScraper correctly generates and rotates headers."""
        scraper = AmazonScraper()

        headers1 = scraper.get_headers()
        headers2 = scraper.get_headers()

        self.assertIn("User-Agent", headers1)
        self.assertIn("User-Agent", headers2)
        self.assertTrue(headers1["User-Agent"].startswith("Mozilla/5.0"))

        self.assertIn("Accept", headers1)
        self.assertIn("Accept-Language", headers1)
        self.assertIn("Connection", headers1)

    def test_amazon_mock_fallback(self):
        """Test that AmazonScraper generates mock reviews correctly when requested."""
        scraper = AmazonScraper()

        limit = 15
        reviews = scraper._generate_mock_reviews("B0BY8MCQ9S", limit)

        self.assertEqual(len(reviews), limit)
        for r in reviews:
            self.assertEqual(r["Product Name"], "Apple iPhone 14 (128 GB) - Blue")
            self.assertIn("Rating", r)
            self.assertIn("Review Text", r)
            self.assertIn("Review Date", r)
            self.assertIn("Reviewer Name", r)
            self.assertTrue(1.0 <= r["Rating"] <= 5.0)

        reviews_generic = scraper._generate_mock_reviews("B000000000", 5)
        self.assertEqual(len(reviews_generic), 5)
        for r in reviews_generic:
            self.assertEqual(r["Product Name"], "Amazon Product (ASIN: B000000000)")

    def test_flipkart_mock_fallback(self):
        """Test that FlipkartScraper generates mock reviews correctly when requested."""
        scraper = FlipkartScraper()

        limit = 10
        reviews = scraper._generate_mock_reviews("apple-iphone-15", "MOBGTAGPAHB5E8AS", limit)

        self.assertEqual(len(reviews), limit)
        for r in reviews:
            self.assertEqual(r["Product Name"], "Apple iPhone 15 (Black, 128 GB)")
            self.assertIn("Rating", r)
            self.assertIn("Review Text", r)
            self.assertIn("Review Date", r)
            self.assertIn("Reviewer Name", r)
            self.assertTrue(1.0 <= r["Rating"] <= 5.0)

        reviews_generic = scraper._generate_mock_reviews("unknown-gadget", "MOB12345", 5)
        self.assertEqual(len(reviews_generic), 5)
        for r in reviews_generic:
            self.assertEqual(r["Product Name"], "Unknown Gadget (ID: MOB12345)")

    def test_data_schema_pandas(self):
        """Test that DataFrame schema can be successfully constructed and validated."""
        scraper = AmazonScraper()
        reviews = scraper._generate_mock_reviews("B0BY8MCQ9S", 5)
        df = pd.DataFrame(reviews)

        required_cols = ["Product Name", "Review Text", "Rating", "Review Date", "Reviewer Name"]
        for col in required_cols:
            self.assertIn(col, df.columns)

        self.assertEqual(len(df), 5)

if __name__ == '__main__':
    unittest.main()
