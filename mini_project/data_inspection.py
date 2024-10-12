import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd


class Inspection:
    def __init__(self):
        self.df = None
        self.column_types = None

    def list_column_types(self) -> dict:
        column_types = dict()
        for column in list(self.df.columns):
            if pd.api.types.is_numeric_dtype(self.df[column]):
                column_types[column] = 'numeric ordinal' if self.df[column].nunique() < 10 else 'interval'
            else:
                column_types[column] = 'non-numeric ordinal' if self.df[column].nunique() < 10 else 'nominal'
        return column_types

    def classify_and_calculate(self, col):
        '''参考上面重写一下'''
        n = self.df[col].nunique()
        if pd.api.types.is_numeric_dtype(self.df[col]):
            if n < 10:  # numeric ordinal
                median_num = self.df[col].median()
                return ['Median', median_num]
            else:  # interval
                mean = self.df[col].mean()
                return ['Mean', mean]
        else:
            if n < 10:  # ordinal
                median_num = self.df[col].median()
                return ['Median', median_num]
            else:  # normal
                mode = self.df[col].mode()[0]
                return ['Mode', mode]

    def plot_histogram(self, data, x_label) -> None:
        plt.figure(figsize=(8, 4))
        sns.histplot(data=data, bins=30, kde=True, color='skyblue', edgecolor='black')
        plt.title(f'Histogram of {x_label}')
        plt.xlabel(x_label)
        plt.ylabel('Frequency')
        plt.show()

    def plot_boxplot(self, x_col, y_col, data) -> None:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=x_col, y=y_col, data=data)
        plt.title(f'Boxplot of {y_col} by {x_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.show()

    def plot_bar_chart(self, x_col, y_col, data) -> None:
        plt.figure(figsize=(8, 4))
        plt.bar(data[x_col], data[y_col], color='skyblue')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'Bar Chart of {x_col} vs {y_col}')
        plt.show()

    def plot_scatter(self, x_col, y_col, data) -> None:
        plt.figure(figsize=(8, 4))
        plt.scatter(data[x_col], data[y_col])
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'Scatter plot of {x_col} vs {y_col}')
        plt.show()

    def plot_QQ_plot(self, data):
        plt.figure(figsize=(8, 4))
        stats.probplot(x=data, dist='norm', plot=plt)
        plt.title('QQ plot')
        plt.show()
