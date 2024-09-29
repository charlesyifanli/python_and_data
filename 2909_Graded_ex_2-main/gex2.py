import pandas as pd
import matplotlib.pyplot as plt
from pygments.styles.dracula import selection


class DataInspection:
    def __init__(self):
        self.df = None  # DataFrame will be loaded and stored here

    def load_csv(self, file_path: str) -> None:
        self.df = pd.read_csv(file_path)

    def plot_histogram(self, col):
        pass

    def plot_boxplot(self, x_col, y_col):
        pass

    def plot_bar_chart(self, col):
        pass

    def plot_scatter(self, x_col, y_col):
        pass

    def handle_missing_values(self, col) -> bool:
        res = True
        percentage = int(self.df[col].isna().sum()) / self.df[col].shape[0]
        if percentage > 0.5:
            self.df = self.df.drop(col, axis=1)
            res = False
        else:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                median_value = self.df[col].median()
                self.df[col] = self.df[col].fillna(median_value)
            else:
                mode_value = self.df[col].mode()[0]
                self.df[col] = self.df[col].fillna(mode_value)
        return res

    def check_data_types(self, col) -> None:
        pass

    def classify_and_calculate(self, col):
        if self.handle_missing_values(col=col):
            # no deleted
            self.check_data_types(col=col)

        else:
            pass

    def classify_columns(self) -> None:
        for column_name in self.df.columns:
            self.classify_and_calculate(col=column_name)

    def ask_for_scatterplot(self):
        pass

    def ask_for_boxplot(self):
        pass

    def numeric_columns(self):
        pass

    def ask_for_correlation(self, numeric_cols):
        pass

    def ask_for_std(self, numeric_cols):
        pass

    def ask_for_kurtosis(self, numeric_cols):
        pass

    def ask_for_skewness(self, numeric_cols):
        pass


# Main function
def main():
    analysis = DataInspection()
    file_path = input('Please enter the path of dataset >> ')

    analysis.load_csv(file_path=file_path)
    analysis.classify_columns()


# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()
