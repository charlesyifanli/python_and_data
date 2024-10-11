import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


class DataAnalysis:
    def __init__(self) -> None:
        self.df = None
        self.column_types = None  ## a dict

    def dataset_loading(self) -> None:
        self.df = pd.read_csv('./test.csv')
        self.column_types = self.list_column_types()

    def list_column_types(self) -> dict:
        column_types = {}
        for column in list(self.df.columns):
            if pd.api.types.is_numeric_dtype(self.df[column]):
                column_types[column] = 'numeric ordinal' if self.df[column].nunique() < 10 else 'interval'
            else:
                column_types[column] = 'non-numeric ordinal' if self.df[column].nunique() < 10 else 'nominal'
        return column_types

    def select_variable(self, data_type, allow_skip=False) -> None or str:
        available_vars = {col: col_type for col, col_type in self.column_types.items() if
                          col_type == data_type or (allow_skip and 'ordinal' in col_type)}
        if not available_vars:
            print(f"No available variables of type {data_type}")
            return None
        else:
            print("Available variables:")
            for col, col_type in available_vars.items():
                print(f"{col}: {col_type}")
            selected_var = input("Please select a variable from the above list: ")
            if selected_var in available_vars:
                return selected_var
            else:
                print("Invalid choice. Please try again.")
                return self.select_variable(data_type, allow_skip)

    def select_ordinal_variable(self) -> None or str:
        all_ordinal_vars = {col: col_type for col, col_type in self.column_types.items() if 'ordinal' in col_type}
        if not all_ordinal_vars:
            print("No available ordinal variables.")
            return None
        else:
            print("Available ordinal variables:")
            for col, col_type in all_ordinal_vars.items():
                print(f"{col}: {col_type}")
            selected_var = input("Please select an ordinal variable from the above list: ")
            if selected_var in all_ordinal_vars:
                return selected_var
            else:
                print("Invalid choice. Please try again.")
                return self.select_ordinal_variable()

    def plot_qq_histogram(self, data, title) -> None:
        fig, axes = plt.subplots(1, 2, figsize=(18, 6))
        # Q-Q plot
        plt.sca(axes[0])
        stats.probplot(x=data, dist='norm', plot=plt)
        plt.title(f'Q-Q Plot of {title}')
        # Histogram
        plt.sca(axes[1])
        plt.hist(data, bins=30, edgecolor='black')
        plt.title(f'Histogram of {title}')
        #
        plt.tight_layout()
        plt.show()

    def check_normality(self, data, size_limit=2000) -> tuple[float, float]:
        data = data.dropna()
        if len(data) <= size_limit:
            print("Shapiro-Wilk Test")
            stat, p_value = stats.shapiro(data)
        else:
            print("Anderson-Darling Test")
            result = stats.anderson(data, dist='norm')
            stat = result.statistic
            p_value = result.significance_level[0]
        return stat, p_value

    def check_skewness(self, data):
        skewness = stats.skew(data.dropna())
        threshold = 0
        return abs(skewness) > threshold

    def hypothesis_test(self, continuous_var, categorical_var, skewed, null_hyp) -> tuple[float, float]:
        print(f"Null Hypothesis: {null_hyp}")
        if skewed:
            # Use Kruskal-Wallis H-test
            stat, p_value = stats.kruskal(
                *[group[continuous_var].values for name, group in self.df.groupby(categorical_var)])
        else:
            # Use ANOVA
            stat, p_value = stats.f_oneway(
                *[group[continuous_var].values for name, group in self.df.groupby(categorical_var)])
        return stat, p_value


def main():
    analysis = DataAnalysis()

    # 1. Dataset is loaded
    analysis.dataset_loading()

    # 2. Ask the user to select a continuous variable, check its normality and visualize it using Q-Q and histogram
    continuous_var = analysis.select_variable('interval')
    if not continuous_var:
        print('No continuous variable selected. Exiting.')
        return

    stat, p_value = analysis.check_normality(analysis.df[continuous_var])
    print(f'Normality test result for {continuous_var}: stat={stat}, p-value={p_value}')
    print(f'{p_value} > 0.05, {continuous_var}: normal' if p_value > 0.05 else f'{continuous_var}: not normal')
    analysis.plot_qq_histogram(analysis.df[continuous_var], continuous_var)

    # 3. Ask the user to select a categorical variable
    categorical_var = analysis.select_variable("nominal", allow_skip=True)
    if not categorical_var:
        print("No categorical variable selected. Exiting.")
        return

    # 4. Calculate skewness of the continuous variable
    skewed = analysis.check_skewness(analysis.df[continuous_var])
    print(f"Skewness of {continuous_var}: {'Highly skewed' if skewed else 'Not highly skewed'}")

    # 5. Ask the user to enter the null hypothesis
    null_hyp = input("Please enter the null hypothesis: ")

    # 6. Conduct the analysis
    stat, p_value = analysis.hypothesis_test(continuous_var=continuous_var, categorical_var=categorical_var,
                                             skewed=skewed, null_hyp=null_hyp)
    print(f"Hypothesis test result: stat={stat}, p-value={p_value}")


if __name__ == "__main__":
    main()
