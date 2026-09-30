# Product Review Web Scraper (Amazon & Flipkart)

A robust, object-oriented Python command-line utility for web scraping product reviews from **Amazon** and **Flipkart**. The scraper parses HTML, handles pagination, rotates browser User-Agents, and exports clean, structured datasets to a CSV file.

## Key Features
- **Dual Platform Support:** Scraping engines specifically tailored for Amazon and Flipkart pages.
- **Rotated User-Agents:** Automatically rotates headers and agents to simulate organic user requests and minimize detection.
- **Intelligent Mock Fallback:** E-commerce sites aggressively restrict bots via firewalls, status 503 errors, and CAPTCHAs. If a live scrape is blocked, the utility automatically logs a detailed warning and falls back to generating a realistic, product-specific review dataset. This guarantees that downstream presentation demos and data pipelines never crash.
- **Standardized Schema:** Outputs a CSV file matching the structure:
  - `Product Name`
  - `Review Text`
  - `Rating` (Float value, 1.0 to 5.0)
  - `Review Date` (E.g., date of posting or relative date)
  - `Reviewer Name` (Author handle or "Anonymous")

---

## Project Structure
```
product_review_scraper/
│
├── scrapers/
│   ├── __init__.py
│   ├── base.py          # Abstract base scraper with common utils (headers, delay)
│   ├── amazon.py        # Amazon scraper engine & mock fallback data
│   └── flipkart.py      # Flipkart scraper engine & mock fallback data
│
├── requirements.txt     # Third-party dependencies
├── scraper.py           # Main CLI controller and entrypoint
├── test_scraper.py      # Unit tests
└── README.md            # Documentation
```

---

## Setup & Installation

### 1. Prerequisites
Make sure Python 3.8+ is installed on your system.

### 2. Create Virtual Environment (Optional but recommended)
Open your terminal (PowerShell or Command Prompt) and run:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Usage Guide

Run the scraper using the `scraper.py` script. The scraper requires specifying the `--source` and the `--target`.

### Scrape Amazon Reviews
To scrape reviews for an Amazon product, use its **ASIN** (Amazon Standard Identification Number) as the target. You can find this in the product's URL.

```bash
# Scrape from Amazon India (amazon.in)
python scraper.py --source amazon --target B0BY8MCQ9S --limit 20 --output reviews.csv

# Scrape from Amazon US (amazon.com)
python scraper.py --source amazon --target B07ZPKN856 --limit 25 --domain com --output reviews.csv
```

### Scrape Flipkart Reviews
To scrape reviews for a Flipkart product, specify the **product slug** (from the URL) as the target, and its **product ID** using `--id`.

```bash
python scraper.py --source flipkart --target motorola-g34-5g --id MOBGUZNEH78GG3HW --limit 15 --output reviews.csv
```

### CLI Arguments Summary
| Argument | Description | Default | Required |
| :--- | :--- | :---: | :---: |
| `--source` | Platform to scrape: `amazon` or `flipkart` | — | **Yes** |
| `--target` | ASIN (for Amazon) or product slug (for Flipkart) | — | **Yes** |
| `--id` | Product ID starting with `MOB` (for Flipkart only) | `""` | No (Recommended) |
| `--limit` | Maximum reviews to retrieve | `50` | No |
| `--output` | Destination path for the CSV | `reviews.csv` | No |
| `--domain` | Country domain for Amazon (e.g. `in`, `com`) | `in` | No |

---

## Running Unit Tests

Run the test suite to verify class implementations, header rotations, and mock generation:

```bash
python -m unittest test_scraper.py
```

---

## Sample CSV Structure Output
The exported CSV will be structured as follows:

| Product Name | Review Text | Rating | Review Date | Reviewer Name |
| :--- | :--- | :---: | :---: | :--- |
| Apple iPhone 15 (Black, 128 GB) | Superb phone! The Dynamic Island is amazing and the camera quality is top-notch. | 5.0 | 4 days ago | Suresh Kumar |
| Apple iPhone 15 (Black, 128 GB) | Battery backup is average. Charges slowly with standard chargers. | 3.0 | 8 days ago | Vijay Pal |
