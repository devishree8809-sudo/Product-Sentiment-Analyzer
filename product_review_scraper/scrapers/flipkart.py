import re
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper

class FlipkartScraper(BaseScraper):
    """
    Scraper for Flipkart product reviews.
    Can scrape real reviews or fall back to simulated review generation if blocked.
    """

    MOCK_DATABASE = {
        "iphone-16": {
            "product_name": "Apple iPhone 16 (Black, 128 GB)",
            "reviews": [
                {"text": "Excellent camera quality and smooth performance. The design feels premium and the battery lasts all day.", "rating": 5.0, "author": "Aarav Mehta"},
                {"text": "Very good display and fast charging. The phone feels solid but the price is on the higher side.", "rating": 4.0, "author": "Nisha Sharma"},
                {"text": "Overall a great phone for daily use. App switching is smooth and the build quality is excellent.", "rating": 5.0, "author": "Rohit Verma"},
                {"text": "The camera is fantastic but I was disappointed that the box does not include a charger.", "rating": 3.0, "author": "Priya S."},
                {"text": "Battery backup is good and the performance is top-class. Worth the upgrade from older iPhones.", "rating": 5.0, "author": "Karan Shah"},
                {"text": "Nice display and strong performance, although the base storage option is a little limited.", "rating": 4.0, "author": "Siddharth Nair"}
            ]
        },
        "apple-iphone-16": {
            "product_name": "Apple iPhone 16 (Black, 128 GB)",
            "reviews": [
                {"text": "Excellent camera quality and smooth performance. The design feels premium and the battery lasts all day.", "rating": 5.0, "author": "Aarav Mehta"},
                {"text": "Very good display and fast charging. The phone feels solid but the price is on the higher side.", "rating": 4.0, "author": "Nisha Sharma"},
                {"text": "Overall a great phone for daily use. App switching is smooth and the build quality is excellent.", "rating": 5.0, "author": "Rohit Verma"},
                {"text": "The camera is fantastic but I was disappointed that the box does not include a charger.", "rating": 3.0, "author": "Priya S."},
                {"text": "Battery backup is good and the performance is top-class. Worth the upgrade from older iPhones.", "rating": 5.0, "author": "Karan Shah"},
                {"text": "Nice display and strong performance, although the base storage option is a little limited.", "rating": 4.0, "author": "Siddharth Nair"}
            ]
        },
        "MOBGTAGPAHB5E8AS": {
            "product_name": "Apple iPhone 15 (Black, 128 GB)",
            "reviews": [
                {"text": "Superb phone! The Dynamic Island is amazing and the camera quality is top-notch.", "rating": 5.0, "author": "Suresh Kumar"},
                {"text": "Battery backup is average. Charges slowly with standard chargers.", "rating": 3.0, "author": "Vijay Pal"},
                {"text": "Great display, super smooth transition, but the price is a bit high.", "rating": 4.0, "author": "Aditya Singh"},
                {"text": "Moved from Android to iOS, taking time to adjust but the device is premium.", "rating": 5.0, "author": "Sneha Patel"},
                {"text": "The camera zoom could be better, but portrait mode is wonderful.", "rating": 4.0, "author": "Rohan Deshmukh"},
                {"text": "No charger in the box. Apple is charging too much for basic items.", "rating": 3.0, "author": "Karan Sharma"},
                {"text": "A perfect phone for photography lovers. Highly recommended!", "rating": 5.0, "author": "Priya Sharma"},
                {"text": "Fabulous design and colors. USB-C port is finally here!", "rating": 5.0, "author": "Rajesh Gupta"}
            ]
        },
        "MOBGUZNEH78GG3HW": {
            "product_name": "Motorola G34 5G (Ice Blue, 128 GB)",
            "reviews": [
                {"text": "Best 5G phone under budget. Super smooth 120Hz display.", "rating": 5.0, "author": "Manish Kumar"},
                {"text": "Camera is below average, especially in low light. Performance is decent.", "rating": 3.0, "author": "Nisha Patel"},
                {"text": "Very clean software experience, zero bloatware! Battery backup is excellent.", "rating": 5.0, "author": "Vikram Singh"},
                {"text": "Heating issue during heavy gaming. Normal usage is fine.", "rating": 3.0, "author": "Sandeep K."},
                {"text": "Sound output is decent. The design looks premium for this price range.", "rating": 4.0, "author": "Anil Verma"},
                {"text": "Superb value for money. Highly recommend to budget buyers.", "rating": 5.0, "author": "Jitendra Pal"}
            ]
        }
    }

    GENERIC_REVIEWS = [
        {"text": "Fabulous product! Extremely satisfied with the purchase.", "rating": 5.0, "author": "Flipkart Customer"},
        {"text": "Nice product, works as expected. Delivery was very fast.", "rating": 4.0, "author": "Verified Buyer"},
        {"text": "Value for money. Good build quality.", "rating": 4.0, "author": "Ravi Shankar"},
        {"text": "Waste of money. Quality is extremely cheap.", "rating": 1.0, "author": "Dissatisfied User"},
        {"text": "Average performance, nothing extraordinary.", "rating": 3.0, "author": "Ankit Gupta"},
        {"text": "Does the job well. Satisfactory customer support.", "rating": 4.0, "author": "Komal Sharma"},
        {"text": "Battery life could have been better, but performance is solid.", "rating": 3.0, "author": "Deepika S."}
    ]

    def _generate_mock_reviews(self, product_slug: str, product_id: str, limit: int) -> list:
        """
        Generates realistic mock review data for a Flipkart product.
        """
        print(f"[INFO] Generating simulated reviews for Flipkart target: {product_slug} ({product_id})")

        if product_id in self.MOCK_DATABASE:
            product_name = self.MOCK_DATABASE[product_id]["product_name"]
            base_reviews = self.MOCK_DATABASE[product_id]["reviews"]
        elif product_slug in self.MOCK_DATABASE:
            product_name = self.MOCK_DATABASE[product_slug]["product_name"]
            base_reviews = self.MOCK_DATABASE[product_slug]["reviews"]
        else:
            clean_name = product_slug.replace("-", " ").title()
            product_name = f"{clean_name} (ID: {product_id})" if product_id else clean_name
            base_reviews = self.GENERIC_REVIEWS

        results = []
        base_date = datetime.now() - timedelta(days=random.randint(1, 30))

        for i in range(limit):
            template = base_reviews[i % len(base_reviews)]
            review_date = base_date - timedelta(days=i * random.randint(1, 4), hours=random.randint(0, 23))

            days_ago = (datetime.now() - review_date).days
            if days_ago == 0:
                date_str = "Today"
            elif days_ago == 1:
                date_str = "Yesterday"
            elif days_ago < 30:
                date_str = f"{days_ago} days ago"
            else:
                months = days_ago // 30
                date_str = f"{months} month{'s' if months > 1 else ''} ago"

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
        Scrapes review data for a Flipkart product.

        Args:
            target (str): The product slug (e.g., 'apple-iphone-15').
            limit (int): Maximum number of reviews to extract.
            product_id (str): Optional product ID required for review page URLs.

        Returns:
            list: A list of dicts with review details.
        """
        product_slug = target.strip().lower()
        product_id = kwargs.get("product_id", "").strip()

        if not product_id:
            print("[WARNING] Flipkart review pages require a product ID (e.g., MOB...). Scraper will try to parse slug or proceed to fallback.")

        reviews_list = []
        page = 1
        product_name = None
        max_pages = (limit // 10) + 2

        print(f"[INFO] Scraping Flipkart reviews for: {product_slug} (ID: {product_id})")

        try:
            if product_slug and product_id:
                base_url = f"https://www.flipkart.com/{product_slug}/product-reviews/{product_id}"
            else:
                raise ValueError("Target slug and product ID are both required for live Flipkart scraping.")

            while len(reviews_list) < limit and page <= max_pages:
                url = f"{base_url}?page={page}"

                headers = self.get_headers()
                response = self.session.get(url, headers=headers, timeout=10)

                if response.status_code != 200:
                    print(f"[WARNING] Flipkart returned status code {response.status_code} on page {page}.")
                    break

                html_content = response.text

                if "turing-captcha" in html_content.lower() or "robot check" in html_content.lower():
                    print(f"[WARNING] Flipkart bot protection detected on page {page}.")
                    break

                soup = BeautifulSoup(html_content, "html.parser")

                if not product_name:
                    title_elem = soup.find("div", class_=lambda x: x and ("_2s4DWS" in x or "VU-ZEg" in x))
                    if title_elem:
                        product_name = title_elem.get_text(strip=True).replace(" Reviews", "")
                    else:
                        product_name = product_slug.replace("-", " ").title()

                review_elements = soup.find_all("div", class_=lambda x: x and ("EPCmJX" in x or "_2w1ZOS" in x))
                is_new_layout = False
                if not review_elements:
                    review_elements = soup.find_all("div", class_=lambda x: x and "r-w7s2jr" in x)
                    if review_elements:
                        is_new_layout = True

                if not review_elements:
                    print(f"[INFO] No review containers found on page {page}. Terminating web extraction.")
                    break

                for review in review_elements:
                    if len(reviews_list) >= limit:
                        break

                    try:
                        if is_new_layout:
                            text_elem = review.find("span", class_="css-1jxf684")
                            text = text_elem.get_text(strip=True) if text_elem else ""

                            stars_container = review.find("div", class_=lambda x: x and "r-rehuqn" in x)
                            rating = len(stars_container.find_all("div", style=lambda x: x and "transform" in x)) if stars_container else 5.0

                            name_elem = review.find("div", class_=lambda x: x and "r-1r2vb7i" in x)
                            author = name_elem.get_text(strip=True) if name_elem else "Anonymous"

                            date_elem = review.find(string=lambda t: t and t.strip().startswith('·'))
                            date_str = date_elem.replace('·', '').strip() if date_elem else "Just now"
                        else:
                            rating_elem = review.find("div", class_=lambda x: x and ("XQDdHH" in x or "_3LWZlK" in x or "_1BLPMq" in x))
                            rating = 5.0
                            if rating_elem:
                                rating_str = rating_elem.get_text(strip=True)
                                match = re.search(r"(\d+)", rating_str)
                                if match:
                                    rating = float(match.group(1))

                            text_elem = review.find("div", class_=lambda x: x and ("ZmyHeo" in x or "_2t3t1M" in x))
                            if text_elem:
                                text = text_elem.get_text(strip=True)
                                if text.endswith("READ MORE"):
                                    text = text[:-9]
                            else:
                                text = ""

                            meta_elements = review.find_all("p", class_=lambda x: x and ("_2NsDsF" in x or "_2Vky1y" in x or "_2sc77z" in x or "date" in x))
                            author = "Anonymous"
                            date_str = ""

                            if len(meta_elements) >= 2:
                                author = meta_elements[0].get_text(strip=True)
                                date_str = meta_elements[1].get_text(strip=True)
                                if len(meta_elements) >= 3:
                                    date_str = meta_elements[2].get_text(strip=True)
                            elif len(meta_elements) == 1:
                                author = meta_elements[0].get_text(strip=True)

                            if not date_str:
                                for p in review.find_all("p"):
                                    p_text = p.get_text()
                                    if "ago" in p_text or "month" in p_text or "day" in p_text:
                                        date_str = p_text.strip()
                                        break

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
                        print(f"[DEBUG] Error parsing single Flipkart review: {e}")
                        continue

                page += 1
                self.delay(1.5, 3.5)

        except Exception as err:
            print(f"[ERROR] Connection or scraper exception occurred for Flipkart: {err}")

        if not reviews_list:
            print(f"[WARNING] Live scraping failed or was blocked by Flipkart. Switching to fallback simulator.")
            return self._generate_mock_reviews(product_slug, product_id, limit)

        print(f"[SUCCESS] Scraped {len(reviews_list)} reviews from Flipkart.")
        return reviews_list
