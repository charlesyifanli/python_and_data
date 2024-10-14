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
        
    def get_text_columns(self):
        
    
    def vader_sentiment_analysis(self, data):
        
    
    def textblob_sentiment_analysis(self, data):
    


    def distilbert_sentiment_analysis(self, data):
        

def main():
    

if __name__ == '__main__':
    main()
