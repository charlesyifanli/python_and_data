import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class DataInspection:
    def __init__(self):
        self.df = None  # DataFrame will be loaded and stored here

    def load_csv(self, file_path: str) -> None:
        self.df = pd.read_csv(file_path)

    def plot_histogram(self, col) -> None:
        plt.hist(self.df[col], bins=20, color='skyblue', edgecolor='black')
        plt.title(f'Histogram of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.show()

    def plot_boxplot(self, x_col, y_col) -> None:
        sns.boxplot(x=x_col, y=y_col, data=self.df)
        plt.title(f'Boxplot of {y_col} by {x_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.show()

    def plot_bar_chart(self, col) -> None:
        value_counts = self.df[col].value_counts()
        plt.bar(value_counts.index, value_counts.values)
        plt.title(f'Bar Chart of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.show()

    def plot_scatter(self, x_col, y_col) -> None:
        plt.scatter(self.df[x_col], self.df[y_col])
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f'Scatter plot of {x_col} vs {y_col}')
        plt.show()

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
        try:
            self.df[col] = pd.to_numeric(self.df[col])
        except ValueError:
            pass

    def classify_and_calculate(self, col) -> int:
        if self.handle_missing_values(col=col):
            self.check_data_types(col=col)
            unique_count = self.df[col].nunique()
            if pd.api.types.is_numeric_dtype(self.df[col]):
                if unique_count < 10:  # Ordinal
                    median_value = self.df[col].median()
                    self.plot_boxplot(col, 3)
                    return median_value
                else:  # Interval/Ratio
                    mean_value = self.df[col].mean()
                    self.plot_histogram(col)
                    return mean_value
            elif pd.api.types.is_object_dtype(self.df[col]):
                if unique_count < 10:  # Ordinal
                    mode_value = self.df[col].mode()[0]
                    self.plot_bar_chart(col)
                    return mode_value
                else:  # Nominal
                    mode_value = self.df[col].mode()[0]
                    self.plot_bar_chart(col)
                    return mode_value
        else:
            return 0

    def classify_columns(self) -> None:
        for column_name in self.df.columns:
            self.classify_and_calculate(col=column_name)

    def ask_for_scatterplot(self) -> None:
        numeric_cols = self.numeric_columns()
        print("Numerical Columns:")
        print(numeric_cols)
        for idx, col in enumerate(numeric_cols, start=1):
            print(f"{idx}. {col}")

        col1_idx = int(input("Select the first column for scatterplot (enter the number): "))
        if col1_idx not in range(len(numeric_cols)):
            col1_idx = 0

        col2_idx = int(input("Select the second column for scatterplot (enter the number): "))
        if col2_idx not in range(len(numeric_cols)):
            col2_idx = 1

        self.plot_scatter(numeric_cols[col1_idx], numeric_cols[col2_idx])

    def ask_for_boxplot(self) -> None:
        numeric_cols = self.numeric_columns()
        ordinal_cols = [col for col in self.df.columns if self.df[col].nunique() < 10]

        print("Numerical Columns:")
        for idx, col in enumerate(numeric_cols, start=1):
            print(f"{idx}. {col}")

        print("Ordinal Columns:")
        for idx, col in enumerate(ordinal_cols, start=1):
            print(f"{idx}. {col}")

        num_col_idx = int(input("Select a numerical column for boxplot (enter the number): ")) - 1
        ord_col_idx = int(input("Select an ordinal column for boxplot (enter the number): ")) - 1

        self.plot_boxplot(numeric_cols[num_col_idx], ordinal_cols[ord_col_idx])

    def numeric_columns(self) -> list[int]:
        numeric_cols = [col for col in self.df.columns if pd.api.types.is_numeric_dtype(self.df[col])]
        return numeric_cols

    def ask_for_correlation(self, numeric_cols) -> None:
        print("Numerical Columns:")
        for idx, col in enumerate(numeric_cols, start=1):
            print(f"{idx}. {col}")

        col1_idx = int(input("Select the first column for correlation (enter the number): ")) - 1
        col2_idx = int(input("Select the second column for correlation (enter the number): ")) - 1

        correlation_value = self.df[numeric_cols[col1_idx]].corr(self.df[numeric_cols[col2_idx]])
        return correlation_value

    def ask_for_std(self, numeric_cols) -> None:
        print("Numerical Columns:")
        for idx, col in enumerate(numeric_cols, start=1):
            print(f"{idx}. {col}")

        col_idx = int(input("Select a column for standard deviation (enter the number): ")) - 1

        std_value = self.df[numeric_cols[col_idx]].std()
        return std_value

    def ask_for_kurtosis(self, numeric_cols) -> None:
        print("Numerical Columns:")
        for idx, col in enumerate(numeric_cols, start=1):
            print(f"{idx}. {col}")

        col_idx = int(input("Select a column for kurtosis (enter the number): ")) - 1

        kurt_value = self.df[numeric_cols[col_idx]].kurt()
        return kurt_value

    def ask_for_skewness(self, numeric_cols) -> None:
        print("Numerical Columns:")
        for idx, col in enumerate(numeric_cols, start=1):
            print(f"{idx}. {col}")

        col_idx = int(input("Select a column for skewness (enter the number): ")) - 1

        skew_value = self.df[numeric_cols[col_idx]].skew()
        return skew_value


# Main function
def main():
    analysis = DataInspection()
    file_path = input('Please enter the path of dataset >> ')

    analysis.load_csv(file_path=file_path)
    analysis.classify_columns()

    analysis.ask_for_scatterplot()
    analysis.ask_for_boxplot()

    numeric_cols = analysis.numeric_columns()

    correlation_value = analysis.ask_for_correlation(numeric_cols)
    print(f"Correlation: {correlation_value}")

    std_value = analysis.ask_for_std(numeric_cols)
    print(f"Standard Deviation: {std_value}")

    kurt_value = analysis.ask_for_kurtosis(numeric_cols)
    print(f"Kurtosis: {kurt_value}")

    skew_value = analysis.ask_for_skewness(numeric_cols)
    print(f"Skewness: {skew_value}")


# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()
