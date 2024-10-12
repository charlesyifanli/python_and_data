from data_analysis import Analysis
from data_inspection import Inspection
import pandas as pd


class Robot:
    def __init__(self):
        self.df = None

    def load_csv(self, file_path):
        self.df = pd.read_csv(file_path)






def main():
    robot = Robot()
    robot.load_csv(input('Please enter the csv file path.'))


if __name__ == '__main__':
    main()
