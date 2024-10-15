from data_analysis import Analysis
from data_inspection import Inspection
from data_clean import Clean
from sentiment_analysis import Sentiment
import pandas as pd


class Robot:
    def __init__(self):
        self.df = None
        self.column_types = None

    def load_csv(self, file_path):
        file_path = './heart_attack_prediction_dataset.csv' if not file_path else file_path
        self.df = pd.read_csv(file_path)


def main():
    ## load data
    robot = Robot()
    robot.load_csv(input('Please enter the csv file path: '))

    ## data cleaning preparation
    clean = Clean(robot.df)
    robot.df = clean.process()

    ## data inspection preparation
    inspection = Inspection(robot.df)
    robot.column_types = inspection.list_column_types()

    ## data analysis preparation
    analysis = Analysis(robot.df, robot.column_types)

    ## sentiment analysis preparation
    sentiment = Sentiment(robot.df)

    ##
    inspection.calculate_and_show()
    while True:
        print(
            '\nWhat do you want to explore?\n1. Plot the data.\n2. Hypothesis testing\n3. Sentiment Analysis.\n4. Quite.')
        choice = input('Please enter the number: ')
        if choice == '1':
            inspection.plot_data()
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            print('\nGood Bye')
            break
        else:
            print('\nInvalid input.')


if __name__ == '__main__':
    main()
