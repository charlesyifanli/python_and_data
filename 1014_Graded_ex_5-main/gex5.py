import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

try:
    from transformers import pipeline
except ImportError:
    pipeline = None


class SentimentAnalysis:
    def __init__(self):
        self.df = None

    def load_data(self, path):
        self.df = pd.read_csv(path)

    def get_text_columns(self):
        text_columns = self.df.select_dtypes(include=['object'])
        data = {
            'Column Name': [],
            'Average Entry Length': [],
            'Unique Entries': []
        }

        for column in text_columns:
            avg_length = text_columns[column].apply(len).mean()
            unique_entries = text_columns[column].nunique()
            data['Column Name'].append(column)
            data['Average Entry Length'].append(avg_length)
            data['Unique Entries'].append(unique_entries)

        result_df = pd.DataFrame(data)
        return result_df

    def vader_sentiment_analysis(self, data):
        analyzer = SentimentIntensityAnalyzer()
        scores = []
        sentiments = []

        for entry in data:
            score = analyzer.polarity_scores(entry)['compound']
            scores.append(score)
            if score >= 0.05:
                sentiments.append('positive')
            elif score <= -0.05:
                sentiments.append('negative')
            else:
                sentiments.append('neutral')

        return scores, sentiments

    def textblob_sentiment_analysis(self, data):
        scores = []
        sentiments = []
        subjectivity = []

        for entry in data:
            analysis = TextBlob(entry)
            polarity = analysis.sentiment.polarity
            subjectivity_score = analysis.sentiment.subjectivity

            scores.append(polarity)
            subjectivity.append(subjectivity_score)

            if polarity > 0:
                sentiments.append('positive')
            elif polarity == 0:
                sentiments.append('neutral')
            else:
                sentiments.append('negative')
        return scores, sentiments, subjectivity

    def distilbert_sentiment_analysis(self, data):
        sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
        scores = []
        sentiments = []

        for entry in data:
            result = sentiment_pipeline(entry)[0]
            score = result['score']
            label = result['label']

            if label in ['4 stars', '5 stars']:
                sentiments.append('positive')
            elif label == '3 stars':
                sentiments.append('neutral')
            else:
                sentiments.append('negative')

            scores.append(score)

        return scores, sentiments


def main():
    sentiment = SentimentAnalysis()

    # Step 2: Ask the user for the path to the data file
    data_path = input("Please enter the path to the data file: ")

    # Step 3: Load the data
    sentiment.load_data(data_path)

    # Step 4: Get text columns and display the DataFrame
    text_columns_df = sentiment.get_text_columns()
    print("Text Columns DataFrame:")
    print(text_columns_df)

    # Step 5: Ask the user to type the column name to be analyzed
    column_name = input("Please enter the column name to be analyzed: ")

    # Step 6: Ask the user to choose the type of sentiment analysis
    print("Choose the type of sentiment analysis:")
    print("1. VADER")
    print("2. TextBlob")
    print("3. DistilBERT")
    choice = input("Enter the number of your choice: ")

    # Step 7: Call the appropriate sentiment analysis function
    if column_name not in sentiment.df.columns:
        print(f"Error: Column '{column_name}' does not exist in the DataFrame.")
        return

    if choice == '1':
        scores, sentiments = sentiment.vader_sentiment_analysis(sentiment.df[column_name])
        result_df = pd.DataFrame({'Score': scores, 'Sentiment': sentiments})
    elif choice == '2':
        scores, sentiments, subjectivity = sentiment.textblob_sentiment_analysis(sentiment.df[column_name])
        result_df = pd.DataFrame({'Score': scores, 'Sentiment': sentiments, 'Subjectivity': subjectivity})
    elif choice == '3':
        scores, sentiments = sentiment.distilbert_sentiment_analysis(sentiment.df[column_name])
        result_df = pd.DataFrame({'Score': scores, 'Sentiment': sentiments})
    else:
        print("Invalid choice. Please restart the program and choose a valid option.")
        return

    # Step 8: Display the resulting DataFrame
    print("Sentiment Analysis Result DataFrame:")
    print(result_df)


if __name__ == '__main__':
    main()
