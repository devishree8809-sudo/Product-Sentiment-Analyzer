import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

df = pd.read_csv("reviews.csv")

def classify_sentiment(review):
    score = analyzer.polarity_scores(str(review))
    compound = score["compound"]

    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Review Text"].apply(classify_sentiment)

df.to_csv("sentiment_results.csv", index=False)

total_reviews = len(df)

positive = (df["Sentiment"] == "Positive").sum()
negative = (df["Sentiment"] == "Negative").sum()
neutral = (df["Sentiment"] == "Neutral").sum()

positive_percentage = (positive / total_reviews) * 100
negative_percentage = (negative / total_reviews) * 100
neutral_percentage = (neutral / total_reviews) * 100

print("\n========== SENTIMENT ANALYSIS ==========")

print(f"Total Reviews       : {total_reviews}")
print(f"Positive Reviews    : {positive} ({positive_percentage:.2f}%)")
print(f"Negative Reviews    : {negative} ({negative_percentage:.2f}%)")
print(f"Neutral Reviews     : {neutral} ({neutral_percentage:.2f}%)")

print("\nOutput file generated successfully!")
print("Saved as sentiment_results.csv")
