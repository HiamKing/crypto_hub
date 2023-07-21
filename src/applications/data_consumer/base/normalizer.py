import re
from pyspark.sql import DataFrame


class DataNormalizer:
    def camel_to_snake(self, name: str) -> str:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def normalize_data(self, df: DataFrame) -> None:
        raise NotImplementedError()

    def save_data(self, df: DataFrame) -> None:
        raise NotImplementedError()
