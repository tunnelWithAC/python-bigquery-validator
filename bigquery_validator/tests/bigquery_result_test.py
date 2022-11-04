import unittest

from bigquery_validator.bigquery_result import BigQueryResult


class BigqueryResultTest(unittest.TestCase):

    def test_query_executes_by_default(self):
        query = "SELECT * FROM `{{ params.project }}.samples.github_timeline` LIMIT 30000"

        bqr = BigQueryResult(query)
        self.assertIsNotNone(bqr.result)

    def test_query_auto_executes_set_to_false_returns_empty_array(self):
        query = "SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`"

        bqr = BigQueryResult(query, auto_execute=False)
        self.assertEqual(bqr.result, [])

    def test_query_metadata_is_not_none(self):
        query = "SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`"

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        unique_rows = len(result_metadata['unique_values']['nrows'])
        total_rows = result_metadata['nrows']
        self.assertIsNotNone(result_metadata)
        self.assertEqual(unique_rows, total_rows)

    def test_query_from_file_metadata_is_not_none(self):
        bqr = BigQueryResult(file_path='./sql/bigquery_result_metadata.sql')
        result_metadata = bqr.metadata()
        unique_rows = len(result_metadata['unique_values']['nrows'])
        total_rows = result_metadata['nrows']
        self.assertIsNotNone(result_metadata)
        self.assertEqual(unique_rows, total_rows)

    def test_query_metadata_returns_correct_columns(self):
        query = '''
        select 'andrew' as name, 21 as age
        union all
        select 'james' as name, 20 as age
        '''

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        columns = result_metadata['columns']
        self.assertEqual(columns, ['name', 'age'])

    def test_query_metadata_returns_correct_unique_values(self):
        query = '''
        select 'andrew' as name, 21 as age
        union all
        select 'james' as name, 20 as age
        '''

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        unique_names = result_metadata['unique_values']['name']
        self.assertEqual(unique_names, ['andrew', 'james'])

    def test_query_from_file_metadata_returns_correct_unique_values(self):
        bqr = BigQueryResult(file_path='./sql/bigquery_result_test.sql')
        result_metadata = bqr.metadata()
        unique_names = result_metadata['unique_values']['name']
        self.assertEqual(unique_names, ['john', 'peter', 'andrew', 'james'])

    def test_query_metadata_returns_correct_null_values(self):
        query = '''
        select 'andrew' as name, null as age
        union all
        select null as name, null as age
        '''

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        null_names = result_metadata['null_values']['name']
        self.assertEqual(null_names, 1)

        null_age = result_metadata['null_values']['age']
        self.assertEqual(null_age, 2)

    def test_query_metadata_returns_correct_value_counts(self):
        query = '''
        select 'andrew' as name, 20 as age
        union all
        select 'john' as name, 20 as age
        '''

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        value_counts = result_metadata['value_counts']
        name_value_counts = value_counts['name']
        self.assertEqual(name_value_counts, {'john': 1, 'andrew': 1})

        age_value_counts = value_counts['age']
        self.assertEqual(age_value_counts, {20: 2})
