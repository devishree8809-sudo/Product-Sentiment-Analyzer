import re
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper

class AmazonScraper(BaseScraper):
    """
    Scraper for Amazon product reviews.
    Can scrape real reviews or fall back to simulated review generation if blocked.
    """

    MOCK_DATABASE = {
        "B0BY8MCQ9S": {
            "product_name": "Apple iPhone 14 (128 GB) - Blue",
            "reviews": [
                {"text": "Excellent camera quality and battery life. Highly recommended!", "rating": 5.0, "author": "Amit Kumar"},
                {"text": "The phone is great, but the charging speed is a bit slow compared to Android devices.", "rating": 4.0, "author": "Neha Sharma"},
                {"text": "Battery drains too fast. Not worth the high price.", "rating": 2.0, "author": "Rahul Verma"},
                {"text": "Value for money product. Premium look and feel.", "rating": 5.0, "author": "Priya Patel"},
                {"text": "Average performance. Nothing spectacular over the iPhone 13.", "rating": 3.0, "author": "Siddharth Sen"},
                {"text": "Decent phone, but screen refresh rate is still 60Hz. Disappointed.", "rating": 3.0, "author": "Vikram Singh"},
                {"text": "Superb display and very fast performance. The A15 chip is still a beast.", "rating": 5.0, "author": "Anjali Gupta"},
                {"text": "Face ID works perfectly. iOS is smooth.", "rating": 5.0, "author": "Rohan Das"},
                {"text": "Sleek design, but extremely expensive accessories.", "rating": 4.0, "author": "Shweta Tiwari"},
                {"text": "Worst experience. Phone got heated up within 10 minutes of gaming.", "rating": 1.0, "author": "Kunal Kapoor"}
            ]
        },
        "B07ZPKN856": {
            "product_name": "Echo Dot (3rd Gen) - Smart speaker with Alexa",
            "reviews": [
                {"text": "Very useful smart speaker. Sound is good for a small room.", "rating": 4.0, "author": "Deepak R."},
                {"text": "Alexa sometimes doesn't understand Indian accent. Otherwise good.", "rating": 3.0, "author": "Karan Johar"},
                {"text": "Absolutely love it! Best budget smart speaker.", "rating": 5.0, "author": "Meera Bai"},
                {"text": "Speaker quality could have been better. Bass is flat.", "rating": 3.0, "author": "Suresh Raina"},
                {"text": "Connecting to Wi-Fi is a nightmare. Keeps disconnecting.", "rating": 2.0, "author": "Vijay Malhotra"},
                {"text": "My kids love asking questions to Alexa. Great educational tool.", "rating": 5.0, "author": "Sunita Rao"},
                {"text": "Excellent integration with my smart home lights.", "rating": 5.0, "author": "Rajesh Nair"},
                {"text": "Too small, volume is low. Go for Echo Plus if you want loud music.", "rating": 3.0, "author": "Preeti Sen"}
            ]
        }
    }

    GENERIC_REVIEWS = [
        {"text": "Absolutely fantastic product! Exceeded my expectations in every way.", "rating": 5.0, "author": "Satisfied Customer"},
        {"text": "Decent quality for the price, but could be improved in terms of durability.", "rating": 3.0, "author": "Smart Shopper"},
        {"text": "Terrible. Broke within the first week of use. Would not recommend.", "rating": 1.0, "author": "Disgruntled Buyer"},
        {"text": "Pretty good, does what it's supposed to do. Fast shipping.", "rating": 4.0, "author": "Alex G."},
        {"text": "Average product. Not bad but not great either. Just okay.", "rating": 3.0, "author": "Chris M."},
        {"text": "High quality materials and works flawlessly. Very pleased.", "rating": 5.0, "author": "Elena R."},
        {"text": "Customer service was very helpful when resolving my issues.", "rating": 4.0, "author": "Marcus Aurelius"},
        {"text": "Too expensive for the value it offers. You can find cheaper alternatives.", "rating": 2.0, "author": "Budget Finder"}
    ]

    def _generate_mock_reviews(self, asin: str, limit: int) -> list:
        """
        Generates realistic mock review data for a given ASIN.
        """
        print(f"[INFO] Generating simulated reviews for ASIN: {asin}")

        if asin in self.MOCK_DATABASE:
            product_name = self.MOCK_DATABASE[asin]["product_name"]
            base_reviews = self.MOCK_DATABASE[asin]["reviews"]
        else:
            product_name = f"Amazon Product (ASIN: {asin})"
            base_reviews = self.GENERIC_REVIEWS

        results = []
        base_date = datetime.now() - timedelta(days=random.randint(1, 30))

        for i in range(limit):
            template = base_reviews[i % len(base_reviews)]
            review_date = base_date - timedelta(days=i * random.randint(1, 3), hours=random.randint(0, 23))
            date_str = f"Reviewed in India on {review_date.strftime('%d %B %Y')}"

            results.append({
                "Product Name": product_name,
                "Review Text": template["text"],
                "Rating": template["rating"],
                "Review Date": date_str,
                "Reviewer Name": template["author"]
            })

        return results

    def scrape(self, target: str, limit: int = 50, **kwargs) -> list:
        """
        Scrapes review data for an Amazon ASIN.

        Args:
            target (str): The Amazon ASIN code.
            limit (int): Maximum number of reviews to extract.
            domain (str): TLD for Amazon (defaults to 'in' for amazon.in).

        Returns:
            list: A list of dicts with review details.
        """
        asin = target.strip().upper()
        domain = kwargs.get("domain", "in")

        reviews_list = []
        page = 1
        product_name = None
        max_pages = (limit // 10) + 2

        print(f"[INFO] Scraping Amazon reviews for ASIN: {asin} via amazon.{domain}")

        try:
            while len(reviews_list) < limit and page <= max_pages:
                url = f"https://www.amazon.{domain}/product-reviews/{asin}/?pageNumber={page}&sortBy=recent"

                headers = self.get_headers()
                response = self.session.get(url, headers=headers, timeout=10)

                if response.status_code != 200:
                    print(f"[WARNING] Amazon returned status code {response.status_code} on page {page}.")
                    break

                html_content = response.text

                if "captcha" in html_content.lower() or "robot check" in html_content.lower():
                    print(f"[WARNING] Amazon robot check / CAPTCHA detected on page {page}.")
                    break

                soup = BeautifulSoup(html_content, "html.parser")

                if not product_name:
                    product_link_elem = soup.find("a", {"data-hook": "product-link"})
                    if product_link_elem:
                        product_name = product_link_elem.get_text(strip=True)
                    else:
                        product_name = f"Amazon Product ({asin})"

                review_elements = soup.find_all("div", {"data-hook": "review"})
                if not review_elements:
                    review_elements = soup.find_all("div", class_="review")

                if not review_elements:
                    print(f"[INFO] No review containers found on page {page}. Terminating web extraction.")
                    break

                for review in review_elements:
                    if len(reviews_list) >= limit:
                        break

                    try:
                        author_elem = review.find("span", class_="a-profile-name")
                        author = author_elem.get_text(strip=True) if author_elem else "Anonymous"

                        rating_elem = review.find("i", {"data-hook": "review-star-rating"})
                        if not rating_elem:
                            rating_elem = review.find("i", {"data-hook": "cmps-review-star-rating"})
                        if not rating_elem:
                            rating_elem = review.find("span", class_="a-icon-alt")

                        rating = 5.0
                        if rating_elem:
                            rating_str = rating_elem.get_text()
                            match = re.search(r"(\d+\.\d+|\d+)", rating_str)
                            if match:
                                rating = float(match.group(1))

                        date_elem = review.find("span", {"data-hook": "review-date"})
                        date_str = date_elem.get_text(strip=True) if date_elem else ""

                        body_elem = review.find("span", {"data-hook": "review-body"})
                        if body_elem:
                            text = body_elem.get_text(strip=True)
                        else:
                            text = ""

                        if not text:
                            continue

                        reviews_list.append({
                            "Product Name": product_name,
                            "Review Text": text,
                            "Rating": rating,
                            "Review Date": date_str,
                            "Reviewer Name": author
                        })

                    except Exception as e:
                        print(f"[DEBUG] Error parsing single review: {e}")
                        continue

                page += 1
                self.delay(1.5, 3.5)

        except Exception as err:
            print(f"[ERROR] Connection or scraper exception occurred: {err}")

        if not reviews_list:
            print(f"[WARNING] Live scraping failed or was blocked by Amazon. Switching to fallback simulator.")
            return self._generate_mock_reviews(asin, limit)

        print(f"[SUCCESS] Scraped {len(reviews_list)} reviews from Amazon.")
        return reviews_list
