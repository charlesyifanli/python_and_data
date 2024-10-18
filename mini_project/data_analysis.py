from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import seaborn as sns


class Analysis:
    def __init__(self, df, types):
        self.df = df
        self.column_types = types

    def analysis_hypothesis(self):
        while True:
            print('\n1. Analyze numeric and category data.\n2. Analyze only category data.\n'
                  '3. Analyze only numeric data.\n4. Back.')
            choice = input('Please enter your choice: ')
            if choice.upper() == '1':
                self.numeric_category_test()
            elif choice.upper() == '2':
                self.category_test()
            elif choice.upper() == '3':
                self.regression_test()
            elif choice.upper() == '4':
                break
            else:
                print('\nInvalid input')

    def numeric_category_test(self):
        numeric_data = self.get_numeric_data()
        print(f'\nNumeric data:')
        for idx, val in enumerate(numeric_data):
            print(f'{idx + 1}: {val}')
        choice_01 = int(input('Please enter the number: '))
        col_01 = numeric_data[choice_01 - 1]

        category_date = self.get_category_data()
        print('\nCategory data: ')
        for idx, val in enumerate(category_date):
            print(f'{idx + 1}: {val}')
        choice_02 = int(input('Please enter the number: '))
        col_02 = category_date[choice_02 - 1]

        ## evaluate
        self.plot_qq_plot(col_01)
        normal_res = self.check_normality(self.df[col_01])
        print('\nNormality Testing:')
        print(f'Null Hypothesis (H₀): The data follows a normal distribution.')
        print('Knowledge: If the data has more than 2000 rows, Anderson-Darling will be suitable, '
              'otherwise, Shapiro-Wilk will be suitable.\n  If p_value > 0.05, fail to reject H0, otherwise, reject H0.')
        print(f'Numeric data: {col_01}')
        print(f'Details: {normal_res}')
        print(f'Numeric data, {col_01}, are normal with p_value > 0.05.'
              if normal_res['is_normal'] == True else f'Numeric data, {col_01}, are not normal with p_value < 0.05.')

        h_res = self.anova_kruskal_t_mann_test(self.df[col_02], self.df[col_01], normal_res['is_normal'])
        print('\nAnova or T Testing:')
        print(f'Null Hypothesis (H0): There is no significant mean/median difference between {col_01} and {col_02}')
        print('Knowledge: If normal data have more than 2 categories, '
              'anova test will be used, otherwise, t-test will be used.'
              '\n  If non normal data have more than 2 categories, '
              'kruskal will be used, otherwise, mann test will be used.')
        print(f'Category data: {col_02}--{self.df[col_02].unique()}')
        print(f'Details: {h_res}')
        print(f'Reject H0 because p-value < 0.05' if h_res['is_significant']
              else 'Fail to reject H0 because p-value > 0.05')

    def category_test(self):
        category_date = self.get_category_data()
        print('\nCategory data: ')
        for idx, val in enumerate(category_date):
            print(f'{idx + 1}: {val}')
        choice_01 = int(input('Please enter the first number: '))
        col_01 = category_date[choice_01 - 1]
        choice_02 = int(input('Please enter the second number: '))
        col_02 = category_date[choice_02 - 1]

        ## evaluate
        chi_res = self.chi_square_test(self.df[col_01], self.df[col_02])
        print('\nChi Square Testing:')
        print(f'Null Hypothesis (H0): There is no significant difference between {col_01} and {col_02}')
        print('\nKnowledge: If p_value > 0.05, fail to reject H0, otherwise, reject H0.')
        print(f'Details: {chi_res}')
        print(f'Reject H0 with p_value < 0.05' if chi_res['is_significant']
              else 'Fail to reject H0 with p value > 0.05')

    def regression_test(self):
        numeric_data = self.get_numeric_data()
        print(f'\nNumeric data:')
        for idx, val in enumerate(numeric_data):
            print(f'{idx + 1}: {val}')
        choice_01 = int(input('Please enter the first number: '))
        col_01 = numeric_data[choice_01 - 1]
        choice_02 = int(input('Please enter the second number: '))
        col_02 = numeric_data[choice_02 - 1]

        x = self.df[[col_01]].values.reshape(-1, 1)
        y = self.df[col_02].values

        ## evaluate
        model = LinearRegression()
        model.fit(x, y)

        print(
            'Knowledge: Positive coefficient: Indicates a positive correlation. When col_01 increases, col_02 also increases.'
            '\n  Negative coefficient: Indicates a negative correlation. When col_01 increases, col_02 decreases.'
            '\n  R-squared: The closer it is to 1, the more effective the model is, and the stronger the relationship between the two variables.')

        print(f'\nRegression results between {col_01} and {col_02}:')
        print(f'Coefficient: {model.coef_[0]}')
        print(f'R-squared: {model.score(x, y)}')

    def check_normality(self, data, critical_size=2000):
        n = len(data)

        if n < critical_size:
            stat, p_value = stats.shapiro(data)
            test_name = 'Shapiro-Wilk'
        else:
            stat, critical_values, significance_level = stats.anderson(data, dist='norm')
            p_value = self.get_ad_p_value(stat, critical_values)
            test_name = 'Anderson-Darling'

        return {
            'test': test_name,
            'statistic': stat,
            'p_value': p_value,
            'is_normal': float(p_value) > 0.05
        }

    @staticmethod
    def anova_kruskal_t_mann_test(category_vars, interval_vars, is_normal=False):
        if category_vars.nunique() < 3:
            if is_normal:
                # Perform t-test
                stat, p_value = stats.ttest_ind(interval_vars[0], interval_vars[1])
                test_name = 't-test'
            else:
                # Perform Mann-Whitney U test
                stat, p_value = stats.mannwhitneyu(interval_vars[0], interval_vars[1])
                test_name = 'Mann-Whitney U'
        else:
            if is_normal:
                # Perform ANOVA
                stat, p_value = stats.f_oneway(*interval_vars)
                test_name = 'ANOVA'
            else:
                # Perform Kruskal-Wallis test
                stat, p_value = stats.kruskal(*interval_vars)
                test_name = 'Kruskal-Wallis'

        return {
            'test': test_name,
            'statistic': stat,
            'p_value': p_value,
            'is_significant': float(p_value) < 0.05
        }

    @staticmethod
    def chi_square_test(var01, var02):
        contingency_table = pd.crosstab(var01, var02)
        stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        # Visualization: Heatmap of the Contingency Table
        plt.figure(figsize=(10, 6))
        sns.heatmap(contingency_table, annot=True, fmt='d', cmap='Blues', cbar=True)
        plt.title('Contingency Table Heatmap')
        plt.xlabel('Variable 2')
        plt.ylabel('Variable 1')
        plt.show()
        ####
        return {
            'test': 'Chi-Square',
            'statistic': stat,
            'p_value': p_value,
            'is_significant': float(p_value) < 0.05
        }

    @staticmethod
    def get_ad_p_value(statistic, critical_values):
        """according to Anderson-Darling statistic and critical_values judge p value"""
        if statistic < critical_values[0]:  # 1% significance level
            return 1.0
        elif statistic < critical_values[1]:  # 5% significance level
            return 0.05
        elif statistic < critical_values[2]:  # 10% significance level
            return 0.01
        return 0.0  # If the statistic exceeds all critical values, the p-value is approximately 0

    def plot_qq_plot(self, col):
        plt.figure(figsize=(8, 4))
        stats.probplot(self.df[col], dist='norm', plot=plt)
        plt.show()

    def get_numeric_data(self):
        return [col for col, category_ in self.column_types.items() if category_ == 'interval']

    def get_category_data(self):
        return [col for col, category_ in self.column_types.items() if category_ != 'interval']
