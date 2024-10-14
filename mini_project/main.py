from data_analysis import Analysis
from data_inspection import Inspection
from data_clean import Clean
from data_sentiment import Sentiment
import pandas as pd


class Robot:
    def __init__(self):
        self.df = None
        self.column_types = None

    def load_csv(self, file_path):
        file_path = './heart_attack_prediction_dataset.csv' if not file_path else file_path
        self.df = pd.read_csv(file_path)


def main():
    robot = Robot()

    ## load data
    robot.load_csv(input('Please enter the csv file path: '))

    ## data cleaning
    clean = Clean()
    clean.df = robot.df
    ### handle missing value and caste type
    clean.process()
    robot.df = clean.df

    ## data inspection
    inspection = Inspection()
    inspection.df = robot.df
    ### classify the data
    inspection.save_column_types()
    robot.column_types = inspection.column_types
    ### visualize and calculate the data
    inspection.calculate_and_plot()
    ### numeric data inspection
    inspection.numeric_data_inspection()
    ### box or scatter
    inspection.box_scatter_plot()

    ## data analysis
    analysis = Analysis()
    analysis.df = robot.df
    analysis.column_types = robot.column_types
    ###
    analysis.analysis_hypothesis()

    ## sentiment analysis
    senti_ana = Sentiment()
    senti_ana.df = robot.df


if __name__ == '__main__':
    main()
