import pandas as pd


class DataAnalysis:
    def __init__(self) -> None:
        self.df = None

    def list_column_types(self) -> dict:
        column_types = dict()
        for column in self.df.columns:
            column_types[column] = self.get_column_type(column)
        return column_types

    def get_column_type(self, column: str) -> str:
        if pd.api.types.is_numeric_dtype(self.df[column]):
            return 'numeric ordinal' if self.df[column].nunique() < 10 else 'interval'
        else:
            return 'non-numeric ordinal' if self.df[column].nunique() < 10 else 'nominal'
