import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd


class Inspection:
    def __init__(self):
        self.df = None
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
