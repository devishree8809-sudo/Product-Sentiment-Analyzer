import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Blueprint, jsonify

_current_dir = os.path.dirname(os.path.abspath(__file__))
_backend_dir = os.path.abspath(os.path.join(_current_dir, ".."))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from services.database_service import database, connect_database

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    from vaderSentiment import SentimentIntensityAnalyzer

_vader_analyzer = SentimentIntensityAnalyzer()

def classify_sentiment_vader(review_text):
    score = _vader_analyzer.polarity_scores(str(review_text))
    compound = score["compound"]
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

try:
    from scrapers.flipkart import FlipkartScraper
except ImportError:
    _scraper_dir = os.path.abspath(os.path.join(_current_dir, "..", "..", "product_review_scraper"))
    if _scraper_dir not in sys.path:
        sys.path.insert(0, _scraper_dir)
    from scrapers.flipkart import FlipkartScraper

analyze_bp = Blueprint("analyze", __name__)

def parse_review_date(date_str):
    if not date_str:
        return datetime(2026, 6, 1)

    date_str = str(date_str).strip()

    match = re.search(r'on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})', date_str)
    if match:
        try:
            return datetime.strptime(match.group(1), "%d %B %Y")
        except ValueError:
            pass

    match = re.search(r'(\d+)\s+days?\s+ago', date_str, re.IGNORECASE)
    if match:
        days = int(match.group(1))
        current_date = datetime(2026, 7, 3)
        return current_date - timedelta(days=days)

    match = re.search(r'(\d+)\s+months?\s+ago', date_str, re.IGNORECASE)
    if match:
        months = int(match.group(1))
        current_date = datetime(2026, 7, 3)
        return current_date - timedelta(days=months * 30)

    if "a month ago" in date_str.lower():
        current_date = datetime(2026, 7, 3)
        return current_date - timedelta(days=30)

    match_my = re.search(r'([A-Za-z]+),?\s+(\d{4})', date_str)
    if match_my:
        month_str = match_my.group(1)
        year_str = match_my.group(2)
        for fmt in ("%b", "%B"):
            try:
                dt_month = datetime.strptime(month_str, fmt)
                return datetime(int(year_str), dt_month.month, 1)
            except ValueError:
                pass

    try:
        return datetime.strptime(date_str, "%d %B %Y")
    except ValueError:
        pass

    return datetime(2026, 6, 1)

def search_flipkart_product(query):
    url = f"https://www.flipkart.com/search?q={re.sub(r'\s+', '+', query.strip())}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a.get("href")
            if "/p/" in href:
                match_item = re.search(r"/p/(itm[a-zA-Z0-9]+)", href)
                match_slug = re.search(r"^/([^/]+)/p/", href)
                if match_item and match_slug:
                    item_id = match_item.group(1)
                    product_slug = match_slug.group(1)
                    return product_slug, item_id
    except Exception as e:
        print(f"[REALTIME ERROR] Flipkart Search Parsing failed: {e}")
    return None

@analyze_bp.route("/analyze/<path:product_name>", methods=["GET"])
def analyze(product_name):
    db = None
    reviews_col = None
    sentiment_col = None
    mongo_available = connect_database()

    if mongo_available:
        try:
            db = database()
            reviews_col = db["Reviews"]
            sentiment_col = db["SentimentResults"]

            query = {"productName": {"$regex": re.escape(product_name), "$options": "i"}}
            reviews = list(reviews_col.find(query))
        except Exception as e:
            print(f"[DB ERROR] Unable to connect to MongoDB for product analysis: {e}")
            reviews = []
            db = None
            reviews_col = None
            sentiment_col = None
    else:
        print("[DB WARNING] MongoDB unavailable. Using local fallback review data.")
        reviews = []

    if not reviews:
        search_res = search_flipkart_product(product_name)
        if search_res:
            slug, item_id = search_res
            print(f"[REALTIME] Found product search result. Slug: {slug}, Item ID: {item_id}")
        else:
            slug = re.sub(r'[^a-zA-Z0-9\s-]', '', product_name).strip().lower()
            slug = re.sub(r'[\s-]+', '-', slug)
            item_id = ""
            print(f"[REALTIME] Product search failed. Using fallback slug: {slug}")

        print(f"[REALTIME] Scraping Flipkart...")
        try:
            scraper = FlipkartScraper()
            scraped_data = scraper.scrape(slug, limit=20, product_id=item_id)
        except Exception as e:
            print(f"[REALTIME ERROR] Scraper failed: {e}")
            scraped_data = []

        if not scraped_data:
            return jsonify({"message": "Product not found"}), 404

        if db is not None:
            products_col = db["Products"]
            product_title = product_name.strip()

            products_col.update_one(
                {"productName": product_title},
                {"$setOnInsert": {"productName": product_title}},
                upsert=True
            )

            for r in scraped_data:
                review_text = r.get("Review Text")
                reviewer = r.get("Reviewer Name", "Anonymous")
                review_date = r.get("Review Date", "Just now")
                rating = float(r.get("Rating", 5.0))

                sentiment_label = classify_sentiment_vader(review_text)

                review_doc = {
                    "productName": product_title,
                    "review": review_text,
                    "rating": rating,
                    "reviewDate": review_date,
                    "reviewerName": reviewer
                }
                exists_review = reviews_col.find_one({
                    "productName": product_title,
                    "review": review_text,
                    "reviewerName": reviewer,
                    "reviewDate": review_date
                })
                if not exists_review:
                    reviews_col.insert_one(review_doc)

                sentiment_doc = {
                    "productName": product_title,
                    "review": review_text,
                    "rating": rating,
                    "reviewDate": review_date,
                    "reviewerName": reviewer,
                    "sentiment": sentiment_label
                }
                sentiment_col.update_one(
                    {
                        "productName": product_title,
                        "review": review_text,
                        "reviewerName": reviewer,
                        "reviewDate": review_date
                    },
                    {"$set": sentiment_doc},
                    upsert=True
                )

            reviews = list(reviews_col.find({"productName": product_title}))
        else:
            product_title = product_name.strip()
            reviews = []
            for r in scraped_data:
                review_text = r.get("Review Text")
                reviewer = r.get("Reviewer Name", "Anonymous")
                review_date = r.get("Review Date", "Just now")
                rating = float(r.get("Rating", 5.0))

                reviews.append({
                    "_id": None,
                    "productName": product_title,
                    "review": review_text,
                    "rating": rating,
                    "reviewDate": review_date,
                    "reviewerName": reviewer
                })

    if not reviews:
        return jsonify({"message": "Product not found"}), 404

    if sentiment_col is None:
        sentiment_lookup = {}
    else:
        reviews_text = [r.get("review") for r in reviews]
        sentiment_query = {"review": {"$in": reviews_text}}
        sentiments = list(sentiment_col.find(sentiment_query))

        sentiment_lookup = {}
        for s in sentiments:
            rev = s.get("review")
            rev_name = s.get("reviewerName")
            if rev and rev_name:
                sentiment_lookup[(rev_name, rev)] = s.get("sentiment", "Neutral")

    positive = 0
    neutral = 0
    negative = 0
    total_rating = 0

    review_list = []
    reviews_by_date = {}

    for review in reviews:
        total_rating += float(review.get("rating", 0))

        sentiment = sentiment_lookup.get((review.get("reviewerName"), review.get("review")))
        if not sentiment:
            sentiment = classify_sentiment_vader(review.get("review"))

        if sentiment.lower() == "positive":
            positive += 1
        elif sentiment.lower() == "negative":
            negative += 1
        else:
            neutral += 1

        review_list.append({
            "id": str(review["_id"]),
            "reviewer": review.get("reviewerName"),
            "text": review.get("review"),
            "rating": review.get("rating"),
            "date": review.get("reviewDate"),
            "sentiment": sentiment
        })

        dt = parse_review_date(review.get("reviewDate"))
        date_key = dt.strftime("%Y-%m-%d")
        if date_key not in reviews_by_date:
            reviews_by_date[date_key] = []
        reviews_by_date[date_key].append(sentiment)

    total = len(review_list)
    average_rating = round(total_rating / total, 1) if total else 0

    sorted_dates = sorted(reviews_by_date.keys())
    timeline_data = []
    cum_pos = 0
    cum_neu = 0
    cum_neg = 0

    for date_str in sorted_dates:
        day_pos = 0
        day_neu = 0
        day_neg = 0
        for sent in reviews_by_date[date_str]:
            if sent.lower() == "positive":
                day_pos += 1
            elif sent.lower() == "negative":
                day_neg += 1
            else:
                day_neu += 1

        cum_pos += day_pos
        cum_neu += day_neu
        cum_neg += day_neg

        dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
        display_date = dt_obj.strftime("%d %b")

        timeline_data.append({
            "date": display_date,
            "positive": cum_pos,
            "neutral": cum_neu,
            "negative": cum_neg
        })

    return jsonify({
        "product_name": reviews[0]["productName"],
        "summary": {
            "total_reviews": total,
            "positive": positive,
            "neutral": neutral,
            "negative": negative,
            "positive_pct": round(positive * 100 / total) if total else 0,
            "neutral_pct": round(neutral * 100 / total) if total else 0,
            "negative_pct": round(negative * 100 / total) if total else 0,
            "average_rating": average_rating
        },
        "reviews": review_list,
        "charts_data": {
            "distribution": [
                {
                    "name": "Positive",
                    "value": positive,
                    "color": "#10B981"
                },
                {
                    "name": "Neutral",
                    "value": neutral,
                    "color": "#F59E0B"
                },
                {
                    "name": "Negative",
                    "value": negative,
                    "color": "#EF4444"
                }
            ],
            "timeline": timeline_data
        }
    })
