# Database Setup — ProductSentimentDB

## Folder structure
```
database/
├── database.py                    <- run this one file to build everything
├── mongodb_connection.py          <- MongoDB connection (edit this to switch local/cloud)
├── import_reviews.py              <- loads reviews.csv
├── import_sentiment.py            <- loads sentiment_results.csv
├── requirements.txt
├── README.md
├── reviews.csv                    <- input from Web Scraping Team
├── sentiment_results.csv          <- input from Sentiment Analysis Team
└── ProductSentimentDB_Export/     <- actual exported data (already generated)
    ├── Reviews.json
    ├── SentimentResults.json
    └── Products.json
```

## Step-by-step: what to do from scratch

### 1. Install MongoDB
- Local option: install MongoDB Community Server and make sure `mongod` is
  running (default: `mongodb://localhost:27017/`).
- Cloud option: create a free MongoDB Atlas cluster and get your connection
  string. Open `mongodb_connection.py` and replace `MONGO_URI` with your
  Atlas string.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Put the CSV files in this folder
Make sure `reviews.csv` (Web Scraping Team) and `sentiment_results.csv`
(Sentiment Analysis Team) are sitting next to `database.py`.

### 4. Run the build
```bash
python database.py
```
This runs all 3 steps in order: test connection -> import reviews -> import
sentiment results. You'll see counts printed at each step.

### 5. Check it worked
```bash
python mongodb_connection.py
```
Should print "Connected successfully to MongoDB."

You can also open MongoDB Compass and look at the `ProductSentimentDB`
database — you should see 3 collections: `Products`, `Reviews`,
`SentimentResults`.

## Verified results (already run against the real data)
| Collection        | Count |
|--------------------|-------|
| Products           | 4     |
| Reviews            | 37    |
| SentimentResults   | 37    |

3 exact duplicate rows were automatically removed from the raw 40-row CSVs.
Reviews and SentimentResults match 1:1 — every review has exactly one
sentiment result.

## About ProductSentimentDB_Export/
These JSON files are a snapshot of what's actually in the database after
running `database.py` — already generated for you. If you ever need to load
this data into a *different* MongoDB instance without re-running the Python
scripts, you can import them directly:
```bash
mongoimport --uri "<your-connection-string>" --db ProductSentimentDB --collection Products --file ProductSentimentDB_Export/Products.json --jsonArray
mongoimport --uri "<your-connection-string>" --db ProductSentimentDB --collection Reviews --file ProductSentimentDB_Export/Reviews.json --jsonArray
mongoimport --uri "<your-connection-string>" --db ProductSentimentDB --collection SentimentResults --file ProductSentimentDB_Export/SentimentResults.json --jsonArray
```

## Handing off to the Backend Team
Give them a small helper (or point them at the `Reviews`/`SentimentResults`
collections directly) using field names: `productName`, `review`, `rating`,
`reviewDate`, `reviewerName`, `sentiment`. These are consistent across all
three collections.
