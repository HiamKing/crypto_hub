import re
from pyspark.sql import DataFrame


class DataNormalizer:
    def camel_to_snake(self, name: str) -> str:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def rename_snake_case_cols(self, df: DataFrame) -> DataFrame:
        renamed_cols = {}
        for col_name in df.columns:
            renamed_cols[col_name] = self.camel_to_snake(col_name)

        n_df = df.withColumnsRenamed(renamed_cols)
        return n_df

    def normalize_data(self, df: DataFrame) -> None:
        raise NotImplementedError()

    def save_data(self, df: DataFrame) -> None:
        raise NotImplementedError()
