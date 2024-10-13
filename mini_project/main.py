from data_analysis import Analysis
from data_inspection import Inspection
from data_clean import Clean
import pandas as pd


class Robot:
    def __init__(self):
        self.df = None
        self.column_types = None

    def load_csv(self, file_path):
        self.df = pd.read_csv('./heart_attack_prediction_dataset.csv')


def main():
    robot = Robot()

    ## load data
    robot.load_csv(input('Please enter the csv file path.'))

    ## data cleaning
    ### handle missing values and caste type
    clean = Clean()
    clean.df = robot.df
    clean.process()
    robot.df = clean.df

    ## data inspection
    ### classify the data
    inspection = Inspection()
    inspection.df = robot.df
    inspection.save_column_types()
    robot.column_types = inspection.column_types
    ### visualize and calculate the data
    # inspection.calculate_and_plot()
    ### numeric data inspection
    inspection.numeric_data_inspection()
    ### box or scatter
    inspection.box_scatter_plot()


if __name__ == '__main__':
    main()
