import math

from google.cloud import bigquery
import pandas as pd

from bigquery_validator import BigQueryValidator


class BigQueryResult:
    """Execute a BigQuery query and extract metadata such total rows and column, unique values in each column, null value
    counts for each column and count of each value in a column.
    """

    def __init__(self,
                 query=None,
                 file_path=None,
                 auto_execute=True,
                 use_query_cache=False):
        self.bq_client = bigquery.Client()
        self.bigquery_validator = BigQueryValidator()

        if file_path is not None and query is not None:
            raise ValueError(
                'Both a query and path to a .sql file were specified.'
                ' Please specify only one of these.')
        elif file_path is None and query is None:
            raise ValueError('A query or path to a .sql file must be specified')
        elif query is not None:
            self.query = self.bigquery_validator.render_templated_query(query)
        else:
            self.query = self.bigquery_validator.render_templated_query_from_file(file_path)

        self.auto_execute = auto_execute
        self.result = []
        self.use_query_cache = use_query_cache

        if self.auto_execute:
            self.execute()

    def execute(self):
        """Execute BigQuery query and returns result as a list of Python dicts"""
        try:
            job_config = bigquery.QueryJobConfig(use_query_cache=self.use_query_cache)
            query_job = self.bq_client.query(self.query, job_config=job_config)
            # todo store query cost
            query_job.result()
            query_result = query_job.result()
            TOTAL_ROWS = query_result.total_rows

            # Get the destination table for the query results.
            # All queries write to a destination table. If a destination table is not
            # specified, then BigQuery populates it with a reference to a temporary
            # anonymous table after the query completes.
            destination = query_job.destination
            destination = self.bq_client.get_table(destination)

            # Retrieve rows and add to result in batches so my laptop doesn't blow up with large result sets
            MAX_RECORDS_PER_BIGQUERY_REQUEST = 10000
            row_iterations = math.ceil(TOTAL_ROWS / MAX_RECORDS_PER_BIGQUERY_REQUEST)
            for i in range(row_iterations):
                rows = self.bq_client.list_rows(destination, max_results=MAX_RECORDS_PER_BIGQUERY_REQUEST)
                for row in rows:
                    self.result.append(dict(row))

            return self.result
        except Exception as e:
            print(e)

    def result(self):
        """Return the result of the query as a Python list"""
        return self.result

    def dataframe(self):
        """Return the result of the query as a dataframe"""
        return pd.DataFrame(self.result)

    def metadata(self):
        """Return additional data related to the result of a query including:
        - nrows: total number of rows in the query result
        - ncols: total number of columns in the query result
        - null_values: count of null values for each column
        - unique_values: the unique values for each column in the result
        - value_counts:  counts of unique values for each column
        """
        df = self.dataframe()

        metadata = {
            'columns': list(df.columns.values),
            'nrows': df.shape[0],
            'ncols': df.shape[1],
            'null_values': {},
            'unique_values': {},
            'value_counts': {}
        }

        for column in df.columns:
            unique_values = list(df[column].unique())
            metadata['unique_values'][column] = unique_values

            null_value_counts = df[column].isna().sum()
            metadata['null_values'][column] = null_value_counts

            value_counts_df = df[column].value_counts()
            value_counts = value_counts_df.to_dict()
            metadata['value_counts'][column] = value_counts
        return metadata
