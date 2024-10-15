import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Inspection:
    def __init__(self, df):
        self.df = df
        self.column_types = None
        self.nominal = None
        self.nu_ordinal = None
        self.na_ordinal = None
        self.interval = None

    def list_column_types(self) -> dict:
        column_types = dict()
        for column in list(self.df.columns):
            if pd.api.types.is_numeric_dtype(self.df[column]):
                column_types[column] = 'numeric ordinal' if self.df[column].nunique() < 10 else 'interval'
            else:
                column_types[column] = 'non-numeric ordinal' if self.df[column].nunique() < 10 else 'nominal'
        self.column_types = column_types
        self.classify_data()
        return column_types

    def classify_data(self):
        self.nominal = [col for col, category in self.column_types.items() if category == 'nominal']
        self.nu_ordinal = [col for col, category in self.column_types.items() if category == 'numeric ordinal']
        self.na_ordinal = [col for col, category in self.column_types.items() if
                           category == 'non-numeric ordinal']
        self.interval = [col for col, category in self.column_types.items() if category == 'interval']

    def calculate_and_show(self):
        data = {
            'Column Name': [],
            'Type': [],
            'Mean': [],
            'Mode': [],
            'Median': [],
            'Std': [],
            'Kurtosis': [],
            'Skewness': []
        }
        for col_name, category in dict(self.column_types).items():
            if 'nominal' in category:
                data['Column Name'].append(col_name)
                data['Type'].append(category)
                data['Mean'].append('NA')
                data['Median'].append('NA')
                data['Mode'].append(self.df[col_name].mode()[0])
                data['Std'].append('NA')
                data['Kurtosis'].append('NA')
                data['Skewness'].append('NA')
            elif 'non-numeric ordinal' in category:
                data['Column Name'].append(col_name)
                data['Type'].append(category)
                data['Mean'].append('NA')
                data['Median'].append('NA')
                data['Mode'].append(self.df[col_name].mode()[0])
                data['Std'].append('NA')
                data['Kurtosis'].append('NA')
                data['Skewness'].append('NA')
            elif 'numeric ordinal' in category:
                data['Column Name'].append(col_name)
                data['Type'].append(category)
                data['Mean'].append('NA')
                data['Mode'].append('NA')
                data['Median'].append(self.df[col_name].median())
                data['Std'].append(self.df[col_name].std())
                data['Kurtosis'].append(self.df[col_name].kurt())
                data['Skewness'].append(self.df[col_name].skew())
            else:
                data['Column Name'].append(col_name)
                data['Type'].append(category)
                data['Mode'].append('NA')
                data['Median'].append('NA')
                data['Mean'].append(self.df[col_name].mean())
                data['Std'].append(self.df[col_name].std())
                data['Kurtosis'].append(self.df[col_name].kurt())
                data['Skewness'].append(self.df[col_name].skew())
        print(pd.DataFrame(data).to_string())

    def plot_data(self):
        while True:
            print('\n1. Bar.\n2. Box.\n3. Histogram.\n4. Scatter.\n5. Quite.')
            choice = input('Please enter the number: ')
            if choice == '1':
                self.plot_bar_chart()
            elif choice == '2':
                self.plot_boxplot()
            elif choice == '3':
                self.plot_histogram()
            elif choice == '4':
                self.plot_scatterplot()
            elif choice == '5':
                break
            else:
                print('\nInvalid input.')

    def plot_bar_chart(self) -> None:
        print('\nNominal data')
        for idx, val in enumerate(self.nominal):
            print(f'{idx + 1}:{val}')
        choice_nominal = self.nominal[int(input('Please enter the number:')) - 1]

        print('\nNumeric data')
        for idx, val in enumerate(self.interval):
            print(f'{idx + 1}:{val}')
        choice_numeric = self.interval[int(input('Please enter the number:')) - 1]

        plt.figure(figsize=(8, 4))
        plt.bar(self.df[choice_nominal], self.df[choice_numeric], color='skyblue')

        plt.title('Bar Chart')
        plt.xlabel(f'{choice_nominal}')
        plt.ylabel(f'{choice_numeric}')

        plt.show()

    def plot_boxplot(self) -> None:
        print('\nOrdinal data')
        for idx, val in enumerate(self.na_ordinal + self.nu_ordinal):
            print(f'{idx + 1}:{val}')
        choice_ordinal = (self.na_ordinal + self.nu_ordinal)[int(input('Please enter the number:')) - 1]

        print('\nNumeric data')
        for idx, val in enumerate(self.interval):
            print(f'{idx + 1}:{val}')
        choice_numeric = self.interval[int(input('Please enter the number:')) - 1]

        plt.figure(figsize=(8, 4))
        sns.boxplot(x=self.df[choice_ordinal], y=self.df[choice_numeric])

        plt.title('Box Plot')
        plt.xlabel(f'{choice_ordinal}')
        plt.ylabel(f'{choice_numeric}')

        plt.show()

    def plot_histogram(self) -> None:
        print('\nNumeric data')
        for idx, val in enumerate(self.interval):
            print(f'{idx + 1}:{val}')
        choice_numeric = self.interval[int(input('Please enter the number:')) - 1]

        plt.figure(figsize=(8, 4))
        sns.histplot(self.df[choice_numeric], kde=True)

        plt.title('Histogram Plot')
        plt.xlabel(f'{choice_numeric}')
        plt.ylabel(f'Frequency')

        plt.show()

    def plot_scatterplot(self):
        print('\nNumeric data')
        for idx, val in enumerate(self.interval):
            print(f'{idx + 1}:{val}')
        choice_numeric = self.interval[int(input('Please enter the number:')) - 1]
        choice_numeric_02 = self.interval[int(input('Please enter the number:')) - 1]

        plt.figure(figsize=(8, 4))
        plt.scatter(x=self.df[choice_numeric], y=self.df[choice_numeric_02])

        plt.title('Scatter Plot')
        plt.xlabel(f'{choice_numeric}')
        plt.ylabel(f'{choice_numeric_02}')

        plt.show()
