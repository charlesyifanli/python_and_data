import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

try:
    from transformers import pipeline
except ImportError:
    pipeline = None


class Sentiment:
    def __init__(self):
        self.df = None
        self.text_df = None

    def load_data(self, path):
        self.df = pd.read_csv(path)

    def analysis(self):
        self.get_text_columns()
        text_list = list(self.text_df.columns)
        print(f'Text columns:')
        for idx, val in enumerate(text_list):
            print(f'{idx + 1}: {val}')
        while True:
            var_num = int(input('Please enter the number'))
            data = self.df[text_list[var_num - 1]]

            choice = input('A. Vader.\nB. TextBlob.\nC.distilbert\nD. Quit')
            if choice.upper() == 'A':
                scores, sentiments = self.vader_sentiment_analysis(data)
                print("Sentiment Analysis Result DataFrame:")
                print(pd.DataFrame({'Score': scores, 'Sentiment': sentiments}))
            elif choice.upper() == 'B':
                scores, sentiments, subjectivity = self.textblob_sentiment_analysis(data)
                print("Sentiment Analysis Result DataFrame:")
                print(pd.DataFrame({'Score': scores, 'Sentiment': sentiments, 'Subjectivity': subjectivity}))
            elif choice.upper() == 'C':
                scores, sentiments = self.distilbert_sentiment_analysis(data)
                print(pd.DataFrame({'Score': scores, 'Sentiment': sentiments}))
            elif choice.upper() == 'D':
                break
            else:
                print('Invalid')
                continue

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

        self.text_df = pd.DataFrame(data)

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
        if pipeline is None:
            raise ImportError("transformers library is not installed")

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