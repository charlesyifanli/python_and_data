import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalysis:
    def __init__(self):
        """Initialize the class with an empty dataset, just like GEX2"""
        

    def dataset_loading(self):
        """Load the dataset from a CSV file."""
        
        self.column_types = """ Also store the list of column types in self.column_types."""
        

    def list_column_types(self):
        """use the same logic as from the GEX2 """
        """This function will check if the type of data is numeric ordinal, non-numeric ordinal, interval, or nominal"""
        """The output will be a dictionary where the key is the column name and the value is the type. wil"""
        
        
        return  """Returning that dictionary"""

    """The following function will ask the user to select one interval and one nominal/ordinal variable"""
    """The function will also allow user to skip selecting a nominal variable and instead select an ordinal variable"""
    def select_variable(self, data_type, allow_skip=False):
        
        available_vars = """First display all the columns that are available in the column_types along with the types"""       

        
        selected_var = """Ask the user to select a variable from the above list"""


        

    """This method will prompt the user to select either a numeric or non-numeric ordinal variable"""
    def select_ordinal_variable(self):
        
        

        all_ordinal_vars = """Store all the numeric and non-numeric ordinal variables here"""

        
        """Print all the available ordinal variables"""
        """Ask the user to pick one"""

        
        """If the user selects a variable from the list of ordinal variables, return that  selected variable"""
        """Otherwise, print invalid choice and call the select_variable method again"""

        
    """The following function simply plots Q-Q and histogram for the chosen variable"""
    def plot_qq_histogram(self, data, title):
        

        plt.show()
    
    
    """This function checks the normality of the variable supplied and comapres it with size_limit to decide 
    if Shapiro-Wilk must be used or Anderson-Darling Test"""
    def check_normality(self, data, size_limit=2000):
        
        """Remember to handle missing values"""
            
        """Based on the size of the data and its comparison with size_limit, do the suitable test for nomality"""
        """Return the stat values and the p-value from whichever test you do"""
        

    

    """This function checks for skewness in your variable. It will return True if the data is highly skewed"""
    def check_skewness(self, data):
        
        return """True if the data is highly skewed"""

    """This function performs either ANOVA or Kruskal-Wallis based on skewness."""
    def hypothesis_test(self, continuous_var, categorical_var, skewed, null_hyp):
        """Regardless of the test you do, the function must return both the statistic and the p-value that every test returns""" 
        
        return """return both the statistic and p-value"""

def main():
    
    analysis = """Create an instance of your class"""

    
    """The main funciton should have the following sequence:
    1. Dataset is loaded
    2. Ask the user to select a continuous variable and then check its normality and visualize it using Q-Q and histogram
    3. Ask the user to select a categorical variable
    4. Calculate skewness of the continuous variable
    5. Ask the user to enter the null hypothesis
    6. Conduct the analysis"""

if __name__ == "__main__":
    main()
