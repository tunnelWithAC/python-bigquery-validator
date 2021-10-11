import unittest

from bigquery_validator.bigquery_result import BigQueryResult


class BigqueryResultTest(unittest.TestCase):

    def test_query_executes_by_default(self):
        query = "SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`"
        bqr = BigQueryResult(query)
        self.assertIsNot(bqr.result(), [])

    def test_query_metadata_is_not_none(self):
        query = "SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`"
        bqr = BigQueryResult(query)
        query_result = bqr.execute()
        # print(query_result)
        df = bqr.dataframe()
        result_metadata = bqr.metadata()
        unique_rows = len(result_metadata['unique_values']['nrows'])
        total_rows = result_metadata['nrows']
        result_unique_values = result_metadata['unique_values']
        result_value_counts = result_metadata['value_counts']
        self.assertIsNotNone(result_metadata)
        self.assertEquals(unique_rows, total_rows)
        # self.assertEquals(result_value_counts, 1)
        # self.assertTrue(valid_sql)