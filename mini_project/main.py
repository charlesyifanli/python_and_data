from data_analysis import Analysis
from data_inspection import Inspection
from data_clean import Clean
import pandas as pd


class Robot:
    def __init__(self):
        self.df = None

    def load_csv(self, file_path):
        self.df = pd.read_csv('./heart_attack_prediction_dataset.csv')


def main():
    robot = Robot()
    clean = Clean()
    inspection = Inspection()

    robot.load_csv(input('Please enter the csv file path.'))

    clean.df = robot.df
    clean.process()
    robot.df = clean.df

    print(robot.df.head())


if __name__ == '__main__':
    main()
