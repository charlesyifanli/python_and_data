import unittest
import pandas as pd
import random
from unittest.mock import patch, MagicMock
import sys

# Mock transformers globally before any other code is imported
sys.modules['transformers'] = MagicMock()

# Now import your student's code after mocking transformers
from gex5 import SentimentAnalysis, main

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

#@patch.dict('sys.modules', {'transformers': MagicMock()})
class TestSentimentAnalysis(unittest.TestCase):
    
    def setUp(self):
        
        self.sa = SentimentAnalysis()
        self.sa.load_data('test.csv')  

        
        self.text_columns = self.sa.get_text_columns()['Column Name'].tolist()

    def test_get_text_columns(self):
        
        result = self.sa.get_text_columns()
        expected_columns = ['Column Name', 'Average Entry Length', 'Unique Entries']
        
        self.assertEqual(list(result.columns), expected_columns)
        print(result)
        
        self.assertGreater(len(result), 2) 

    def test_vader_sentiment_analysis(self):
        
        text_column = random.choice(self.text_columns)
        scores, sentiments = self.sa.vader_sentiment_analysis(self.sa.df[text_column])

        self.assertEqual(len(scores), len(self.sa.df[text_column]))
        self.assertLess(abs(sum(scores)/len(scores)), 0.12)
        self.assertEqual(len(sentiments), len(self.sa.df[text_column]))

    def test_textblob_sentiment_analysis(self):
        
        text_column = random.choice(self.text_columns)
        scores, sentiments, subjectivity = self.sa.textblob_sentiment_analysis(self.sa.df[text_column])
        
        
        self.assertEqual(len(scores), len(self.sa.df[text_column]))
        self.assertLess(abs(sum(scores)/len(scores)), 0.43)
        self.assertEqual(len(sentiments), len(self.sa.df[text_column]))

    def test_distilbert_sentiment_analysis(self):
    # Correctly patching the pipeline in the gex5 module, ensuring it's callable
        with patch('gex5.pipeline') as mock_pipeline:
            # Mock the return value of the pipeline when it is called
            mock_pipeline.return_value = MagicMock(return_value=[{'label': '5 stars', 'score': 0.98}])
    
            # Now, proceed with the test
            text_column = random.choice(self.text_columns)
            scores, sentiments = self.sa.distilbert_sentiment_analysis(self.sa.df[text_column])
    
            # Assertions to validate results
            self.assertEqual(len(scores), len(self.sa.df[text_column]))
            self.assertLess(abs(sum(scores)/len(scores)), 0.99)
            self.assertEqual(len(sentiments), len(self.sa.df[text_column]))
        
    @patch('builtins.input')
    @patch('builtins.print')  
    def test_main(self, mock_print, mock_input):
        
        csv_input = 'test.csv'
        column_input = random.choice(self.text_columns)  
        analyzer_input = str(random.choice([1, 2, 3]))  

        mock_input.side_effect = [csv_input, column_input, analyzer_input]
        
        main()  

        self.assertEqual(mock_input.call_count, 3)
        
        
        self.assertTrue(mock_print.called)


if __name__ == '__main__':
    unittest.main()