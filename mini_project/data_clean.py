import pandas as pd


class Clean:
    def __init__(self, df):
        self.df = df

    def process(self):
        for col in self.df.columns:
            self.handle_missing_values(col)
            self.check_data_types(col)
        return self.df

    def handle_missing_values(self, col) -> bool:
        percentage = self.df[col].isna().mean()
        if percentage > 0.5:
            self.df.drop(col, axis=1, inplace=True)
            return False
        fill_value = self.df[col].median() if pd.api.types.is_numeric_dtype(self.df[col]) else self.df[col].mode()[0]
        self.df[col] = self.df[col].fillna(fill_value)
        return True

    def check_data_types(self, col) -> None:
        try:
            self.df[col] = pd.to_numeric(self.df[col])
        except ValueError:
            pass
