import pandas as pd
from AnalysisTools import AnalysisTools
from scipy.stats import linregress


class DataAnalysis:
    def __init__(self):
        self.df = None

    def dataset_loading(self):
        self.df = pd.read_csv('./test.csv')

    def list_column_types(self):
        column_types = dict()
        for column in list(self.df.columns):
            if pd.api.types.is_numeric_dtype(self.df[column]):
                column_types[column] = 'numeric ordinal' if self.df[column].nunique() < 10 else 'interval'
            else:
                column_types[column] = 'non-numeric ordinal' if self.df[column].nunique() < 10 else 'nominal'
        return column_types

    def select_variable(self, data_type, max_categories=None, allow_skip=False):
        column_types = self.list_column_types()
        filtered_columns = {col: col_type for col, col_type in column_types.items() if data_type in col_type}

        if max_categories is not None:
            filtered_columns = {col: col_type for col, col_type in filtered_columns.items() if
                                self.df[col].nunique() <= max_categories}

        if not filtered_columns:
            print(f"No available {data_type} variables with the specified criteria.")
            return None

        print(f"Available {data_type} variables:")
        for col, col_type in filtered_columns.items():
            print(f"{col}: {col_type}")

        while True:
            selected_var = input("Please select a variable from the above list: ")
            if selected_var in filtered_columns:
                return selected_var
            elif allow_skip and selected_var.lower() == 'skip':
                return None
            else:
                print("Invalid choice. Please try again.")

    def check_normality(self, data, size_limit=2000):
        dict_ = AnalysisTools.check_normality(data=data, critical_size=size_limit)
        return dict_['statistic'], dict_['p_value']

    def perform_regression(self, x_var, y_var):
        X = self.df[x_var].dropna()
        Y = self.df[y_var].dropna()

        min_length = min(len(X), len(Y))
        X = X[:min_length]
        Y = Y[:min_length]

        slope, intercept, r_value, p_value, std_err = linregress(X, Y)

        print(f"Slope: {slope:.4f}")
        print(f"Intercept: {intercept:.4f}")
        print(f"R-squared: {r_value ** 2:.4f}")
        print(f"P-value: {p_value:.15f}")
        print(f"Standard error: {std_err:.4f}")

    def t_test_or_mannwhitney(self, continuous_var, categorical_var):
        normality = AnalysisTools.check_normality(data=continuous_var)
        test_dict = AnalysisTools.anova_kruskal_t_mann_test(category_vars=categorical_var,
                                                            interval_vars=continuous_var,
                                                            is_normal=normality['is_normal'])
        return test_dict['statistic'], test_dict['p_value']

    def chi_square_test(self, categorical_var_1, categorical_var_2):
        tool = AnalysisTools().chi_square_test(self.df[categorical_var_1], self.df[categorical_var_2])
        print(f"chi2 = {tool['statistic']:.4f}")
        print(f"p-value = {tool['p_value']:.15f}")
        return tool['statistic'], tool['p_value']


def main():
    analysis = DataAnalysis()
    analysis.dataset_loading()

    while True:
        print("Choose an analysis to perform:")
        print("1. t-test or Mann-Whitney U Test")
        print("2. Chi-square Test")
        print("3. Linear Regression")
        print("Enter 'q' to quit.")

        choice = input("Your choice: ").strip()

        if choice.lower() == 'q':
            break

        if choice == '1':
            nominal_vars = analysis.select_variable('nominal', max_categories=2)
            if not nominal_vars:
                print("No suitable nominal variables with 2 or fewer categories for t-Test or Mann-Whitney U Test.")
                continue

            continuous_vars = analysis.select_variable('interval')
            if not continuous_vars:
                print("No suitable continuous variables for the analysis.")
                continue

            test_choice = input("Choose test: 1 for t-test, 2 for Mann-Whitney U Test: ").strip()
            if test_choice == '1':
                statistic, p_value = analysis.t_test_or_mannwhitney(continuous_vars, nominal_vars)
                print(f"t-Test Statistic: {statistic:.4f}, p-value: {p_value:.15f}")
            elif test_choice == '2':
                statistic, p_value = analysis.t_test_or_mannwhitney(continuous_vars, nominal_vars)
                print(f"Mann-Whitney U Test Statistic: {statistic:.4f}, p-value: {p_value:.15f}")
            else:
                print("Invalid choice.")

        elif choice == '2':
            nominal_vars = analysis.select_variable('nominal')
            if not nominal_vars or len(nominal_vars) < 2:
                print("No suitable nominal variables for Chi-square Test.")
                continue

            var1 = analysis.select_variable('nominal')
            var2 = analysis.select_variable('nominal')
            if var1 and var2:
                statistic, p_value = analysis.chi_square_test(var1, var2)
                print(f"Chi-square Test Statistic: {statistic:.4f}, p-value: {p_value:.15f}")

        elif choice == '3':
            continuous_vars = analysis.select_variable('interval', allow_skip=True)
            if not continuous_vars:
                print("Not enough continuous variables for Linear Regression.")
                continue

            continuous_var2 = analysis.select_variable('interval', allow_skip=True)
            if continuous_var2 and continuous_var2 != continuous_vars:
                analysis.perform_regression(continuous_vars, continuous_var2)
            else:
                print("You need to select a different continuous variable.")

        else:
            print("Invalid choice. Please select 1, 2, 3, or 'q' to quit.")


if __name__ == "__main__":
    main()
