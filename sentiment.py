from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER if not already available
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob and VADER."""
    blob_score = TextBlob(text).sentiment.polarity  # -1 (negative) to 1 (positive)
    vader_score = sia.polarity_scores(text)["compound"]  # -1 to 1

    avg_score = (blob_score + vader_score) / 2  # Average the scores

    if avg_score > 0.3:
        return "positive"
    elif avg_score < -0.3:
        return "negative"
    else:
        return "neutral"
