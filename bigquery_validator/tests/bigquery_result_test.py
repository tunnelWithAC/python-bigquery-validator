import unittest

from bigquery_validator.bigquery_result import BigQueryResult


class BigqueryResultTest(unittest.TestCase):

    def test_query_executes_by_default(self):
        query = "SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`"

        bqr = BigQueryResult(query)
        print(bqr.result)
        self.assertIsNotNone(bqr.result)

    def test_query_auto_executes_set_to_false_returns_empty_arrya(self):
        query = "SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`"

        bqr = BigQueryResult(query, auto_execute=False)
        self.assertEquals(bqr.result, [])

    def test_query_metadata_is_not_none(self):
        query = "SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`"

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        unique_rows = len(result_metadata['unique_values']['nrows'])
        total_rows = result_metadata['nrows']
        self.assertIsNotNone(result_metadata)
        self.assertEquals(unique_rows, total_rows)

    def test_query_from_file_metadata_is_not_none(self):
        bqr = BigQueryResult(file_path='./sql/bigquery_result_metadata.sql')
        result_metadata = bqr.metadata()
        unique_rows = len(result_metadata['unique_values']['nrows'])
        total_rows = result_metadata['nrows']
        self.assertIsNotNone(result_metadata)
        self.assertEquals(unique_rows, total_rows)

    def test_query_returns_correct_number_of_unique_values(self):
        query = '''
        SELECT distinct(repository_url)
        FROM `bigquery-public-data.samples.github_timeline`
        LIMIT 5
        '''

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        unique_rows = len(result_metadata['unique_values']['repository_url'])
        self.assertEquals(unique_rows, 5)

    def test_query_from_file_returns_correct_number_of_unique_values(self):
        bqr = BigQueryResult(file_path='./sql/bigquery_result_test.sql')
        result_metadata = bqr.metadata()
        unique_rows = len(result_metadata['unique_values']['repository_url'])
        self.assertEquals(unique_rows, 5)
