from scipy import stats


class DataAnalysis:
    def __init__(self) -> None:
        self.df = None

    def check_normality(self, data) -> dict:
        n = len(data)

        if n < 50:
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
            'is_normal': p_value > 0.05
        }

    def get_ad_p_value(self, statistic, critical_values) -> float:
        """according to Anderson-Darling statistic and critical_values judge p value"""
        if statistic < critical_values[0]:  # 1% significance level
            return 1.0
        elif statistic < critical_values[1]:  # 5% significance level
            return 0.05
        elif statistic < critical_values[2]:  # 10% significance level
            return 0.01
        return 0.0  # If the statistic exceeds all critical values, the p-value is approximately 0
