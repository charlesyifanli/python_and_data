import io
import unittest
from unittest.mock import patch
import pandas as pd
from gex3 import DataAnalysis  

class TestDataAnalysis(unittest.TestCase):
    def setUp(self):
        
        self.analysis = DataAnalysis()
        self.analysis.df = pd.read_csv('test.csv')  
        self.analysis.column_types = self.analysis.list_column_types()

    @patch('builtins.input', side_effect=['score'])
    def test_select_variable(self, mock_input):
        
        selected_var = self.analysis.select_variable("interval")
        self.assertEqual(selected_var, 'score', "The selected variable should be 'score'.")

    @patch('builtins.input', side_effect=['group'])
    def test_select_ordinal_variable(self, mock_input):
        
        selected_var = self.analysis.select_ordinal_variable()
        self.assertEqual(selected_var, 'group', "The selected ordinal variable should be 'group'.")

    def test_check_normality(self):
        
        # We choose the 'score' column for normality testing
        with patch('sys.stdout', new_callable=lambda: io.StringIO()) as mock_stdout:
            self.analysis.check_normality(self.analysis.df['score'])  # Assuming 'score' is a column in the test.csv
            output = mock_stdout.getvalue()

        # Check for presence of "Shapiro-Wilk Test" in the output
        self.assertIn("Shapiro-Wilk Test", output, "Shapiro-Wilk test should be run on 'score'.")

    def test_hypothesis_test_anova(self):
        
        continuous_var = 'score'  # Adjust this to match your actual data
        categorical_var = 'group'  # Adjust this to match your actual data
        skewed = False
        null_hyp = "There is no difference in score between group groups."

        # Run hypothesis test
        stat, p_value = self.analysis.hypothesis_test(continuous_var, categorical_var, skewed, null_hyp)

        # Verify that p-value is within a valid range (0 to 1)
        self.assertGreaterEqual(p_value, 0, "p-value should be a valid float number.")
        self.assertLessEqual(p_value, 1, "p-value should be a valid float number.")


    def test_hypothesis_test_kruskal(self):
        
        continuous_var = 'score'
        categorical_var = 'group'
        skewed = True
        null_hyp = "There is no difference in score between group groups."
        
        # Run hypothesis test
        stat, p_value = self.analysis.hypothesis_test(continuous_var, categorical_var, skewed, null_hyp)
        
        self.assertGreaterEqual(p_value, 0, "p-value should be a valid float number.")
        self.assertLessEqual(p_value, 1, "p-value should be a valid float number.")

if __name__ == '__main__':
    unittest.main()
