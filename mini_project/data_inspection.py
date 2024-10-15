import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Inspection:
    def __init__(self, df):
        self.df = df
        self.column_types = None

    def save_column_types(self):
        self.column_types = self.list_column_types()

    def list_column_types(self) -> dict:
        column_types = dict()
        for column in list(self.df.columns):
            if pd.api.types.is_numeric_dtype(self.df[column]):
                column_types[column] = 'numeric ordinal' if self.df[column].nunique() < 10 else 'interval'
            else:
                column_types[column] = 'non-numeric ordinal' if self.df[column].nunique() < 10 else 'nominal'
        return column_types

    def calculate_and_plot(self):
        for col_name, category in dict(self.column_types).items():
            if 'nominal' in category:
                mode = self.df[col_name].mode()[0]
                self.plot_bar_chart(col_name, mode)
            elif 'non-numeric' in category:
                mode = self.df[col_name].mode()[0]
                self.plot_bar_chart(col_name, mode)
            elif 'numeric' in category:
                median = self.df[col_name].median()
                self.plot_boxplot(col_name, median)
            else:
                mean = self.df[col_name].mean()
                self.plot_histogram(col_name, mean)

    def plot_bar_chart(self, col, mode) -> None:
        res = self.df[col].value_counts()

        plt.figure(figsize=(8, 4))
        plt.bar(res.index, res.values, color='skyblue')

        plt.title('Category Frequency')
        plt.xlabel('Category')
        plt.ylabel('Count')

        plt.legend([f'Mode: {mode}'], loc='upper right')
        plt.show()

    def plot_boxplot(self, col, median) -> None:
        plt.figure(figsize=(8, 4))
        sns.boxplot(y=self.df[col])
        plt.title(f'Boxplot of {col}')
        plt.xlabel('')
        plt.ylabel(col)

        plt.legend([f'Median: {median}'], loc='upper right')
        plt.show()

    def plot_histogram(self, col, mean) -> None:
        plt.figure(figsize=(8, 4))
        sns.histplot(data=self.df[col], bins=30, kde=True, color='skyblue', edgecolor='black')

        plt.title(f'Histogram of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')

        plt.legend([f'Mean: {mean}'], loc='upper right')
        plt.show()

    def numeric_data_inspection(self):
        numeric_data = [col for col, category in self.column_types.items() if category == 'interval']
        print(f'Numerical data:')
        for idx, val in enumerate(numeric_data):
            print(f'{idx + 1}: {val}')
        while True:
            print('A. Inspect only one var.\nB. Inspect two vars relationship.\nC. Quit.')
            choice = input('Please enter your choice only with "A" "B" or "C": ')
            if choice.upper() == 'A':
                select = int(input('Please enter the var number: '))
                idx = select - 1
                col = numeric_data[idx]
                print(f'Your choice is {col}')
                print(f'Std: {self.df[col].std()}\nKurtosis: {self.df[col].kurt()}\nSkewness:{self.df[col].skew()}')
            elif choice.upper() == 'B':
                select_01 = int(input('Please enter the fist number: '))
                select_02 = int(input('Please enter the second number: '))
                col_01 = numeric_data[select_01 - 1]
                col_02 = numeric_data[select_02 - 1]
                print(f'Your choice is {col_01} and {col_02}')
                print(f'Correlation: {self.df[col_01].corr(self.df[col_02])}')
            elif choice.upper() == 'C':
                break
            else:
                print('Invalid')
                continue

    def box_scatter_plot(self):
        category_data = [col for col, category in self.column_types.items() if category != 'interval']
        numeric_data = [col for col, category in self.column_types.items() if category == 'interval']
        while True:
            print('A. Box.\nB. Scatter.\nC. Quit.')
            choice = input('Please enter your choice only with "A" "B" or "C": ')
            if choice.upper() == 'A':
                print(f'Category data:')
                for idx, val in enumerate(category_data):
                    print(f'{idx + 1}: {val}')
                select_01 = int(input('Please enter the category data number: '))
                col_01 = category_data[select_01 - 1]

                print(f'Numerical data:')
                for idx, val in enumerate(numeric_data):
                    print(f'{idx + 1}: {val}')
                select_02 = int(input('Please enter the numeric data number: '))
                col_02 = numeric_data[select_02 - 1]
                ##
                self.plot_boxplot_02(col_01, col_02)
            elif choice.upper() == 'B':
                print(f'Numerical data:')
                for idx, val in enumerate(numeric_data):
                    print(f'{idx + 1}: {val}')
                select_01 = int(input('Please enter the fist number: '))
                select_02 = int(input('Please enter the second number: '))
                col_01 = numeric_data[select_01 - 1]
                col_02 = numeric_data[select_02 - 1]
                ##
                self.plot_scatterplot(col_01, col_02)
            elif choice.upper() == 'C':
                break
            else:
                print('Invalid')
                continue

    def plot_boxplot_02(self, col_01, col_02):
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=self.df[col_01], y=self.df[col_02])

        plt.title(f'Boxplot of {col_01} by {col_02}')
        plt.xlabel(col_01)
        plt.ylabel(col_02)

        plt.show()

    def plot_scatterplot(self, col_01, col_02):
        plt.figure(figsize=(8, 4))
        plt.scatter(x=self.df[col_01], y=self.df[col_02])

        plt.title(f'Scatter of {col_01} and {col_02}')
        plt.xlabel(col_01)
        plt.ylabel(col_02)

        plt.show()
