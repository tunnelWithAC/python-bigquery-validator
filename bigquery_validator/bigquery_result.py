from google.cloud import bigquery
import pandas as pd

from bigquery_validator import BigQueryValidator


class BigQueryResult:

    def __init__(self,
                 query,
                 auto_execute=True,
                 use_query_cache=False):
        self.bq_client = bigquery.Client()
        self.bigquery_validator = BigQueryValidator()
        self.query = self.bigquery_validator.render_templated_query(query)
        self.auto_execute = auto_execute
        self.result = []
        self.use_query_cache = use_query_cache

        if self.auto_execute:
            self.execute()

    def execute(self):
        try:
            job_config = bigquery.QueryJobConfig(use_query_cache=self.use_query_cache)
            query_result = self.bq_client.query(self.query, job_config=job_config)
            self.result = [dict(r) for r in query_result]
            return self.result
        except Exception as e:
            print(e)

    def result(self):
        return self.result

    def dataframe(self):
        return pd.DataFrame(self.result)

    def metadata(self):
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
        df = self.dataframe()

        metadata = {
            'nrows': df.shape[0],
            'ncols': df.shape[1],
            'null_values': {},
            'unique_values': {},
            'value_counts': {}
        }

        for column in df.columns:
            unique_values = df[column].unique()
            metadata['unique_values'][column] = unique_values

            null_value_counts = df[column].isnull()  # isna().sum()
            metadata['null_values'][column] = null_value_counts

            value_counts_df = df[column].value_counts()
            value_counts = value_counts_df.to_dict()
            metadata['value_counts'][column] = value_counts
        return metadata

