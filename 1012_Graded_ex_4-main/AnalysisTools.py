from scipy import stats
import pandas as pd


class AnalysisTools:
    @staticmethod
    def check_normality(data, critical_size=2000):
        n = len(data)

        if n < critical_size:
            stat, p_value = stats.shapiro(data)
            test_name = 'Shapiro-Wilk'
        else:
            stat, critical_values, significance_level = stats.anderson(data, dist='norm')
            p_value = AnalysisTools.get_ad_p_value(stat, critical_values)
            test_name = 'Anderson-Darling'

        return {
            'test': test_name,
            'statistic': stat,
            'p_value': p_value,
            'is_normal': float(p_value) > 0.05
        }

    @staticmethod
    def anova_kruskal_t_mann_test(category_vars, interval_vars, is_normal=False):
        if len(category_vars) < 3:
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
