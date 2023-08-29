from textblob import TextBlob


def perform_sentiment_analysis(text):
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        print(sentiment)


if __name__ == "__main__":
     perform_sentiment_analysis("WOW its so good")