from google.cloud import bigquery
import pandas as pd


class BigQueryResult:

    def __init__(self,
                 query,
                 use_query_cache):
        self.bq_client = bigquery.Client()
        self.query = query
        self.result = []
        self.use_query_cache = use_query_cache

    def execute(self):
        try:
            job_config = bigquery.QueryJobConfig(use_query_cache=self.use_query_cache)
            self.result = self.bq_client.query(self.query, job_config=job_config)
        except Exception as e:
            print(e)

    def result(self):
        return self.result()

    def dataframe(self):
        return pd.DataFrame(self.result())

    def metadata(self):
        df = self.dataframe()

        metadata = {
            'null_values': {},
            'unique_values': {},
            'value_counts': {}
        }

        for column in df.columns:
            unique_values = df[column].unique_values()
            metadata['unique_values'][column] = unique_values

            null_value_counts = df[column].isnull()  # isna().sum()
            metadata['null_values'][column] = null_value_counts

            value_counts_df = df[column].value_counts
            value_counts = value_counts_df.to_dict(orient='records')
            metadata['value_counts'][column] = value_counts
        return metadata

    """
    Result: python list of rows
    dataframe(): result as a dataframe
    metadata(): data for each column including
    - unique values
    - null values count
    - has null values
    - has non null values
    - count each value
    """