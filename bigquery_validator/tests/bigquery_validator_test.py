from datetime import datetime, timedelta
import os
import sys
import unittest

from bigquery_validator.bigquery_validator import BigQueryValidator


sys.path.append(os.getcwd())

class BigqueryValidatorTest(unittest.TestCase):

    bigquery_validator = BigQueryValidator()

    def test_valid_query_returns_true(self):
        query = "SELECT count(*) FROM `bigquery-public-data.samples.github_timeline`"
        valid_sql, _ = self.bigquery_validator.validate_query(query)
        self.assertTrue(valid_sql)

    def test_bad_query_returns_false(self):
        query = "SELECT count(*) ROM `bigquery-public-data.samples.github_timeline`"
        bad_sql, _ = self.bigquery_validator.validate_query(query)
        self.assertFalse(bad_sql)

    def test_valid_query_from_file_returns_true(self):
        valid_sql, _ = self.bigquery_validator.validate_query_from_file("./valid_query.sql")
        self.assertTrue(valid_sql)

    def test_bad_query_from_file_returns_false(self):
        bad_sql, _ = self.bigquery_validator.validate_query_from_file("./bad_query.sql")
        self.assertFalse(bad_sql, 'assert_bad_sql_from_file_fails_validation')

    def test_extra_params_are_loaded_from_file(self):
        print(self.bigquery_validator.params)
        import importlib.util
        print(importlib.util.find_spec('query_validator_config'))

        if importlib.util.find_spec('query_validator_config') is not None:
            from query_validator_config import params as extra_params
            print(extra_params)
        test_param = self.bigquery_validator.params.get('environment')
        self.assertEqual(test_param, 'test', 'assert_extra_param_exists')

    # def test_parameterize_sql_formats_default_param_correctly(self):
    #     now = datetime.now() - timedelta(days=1)
    #     ds = now.strftime('%Y-%m-%d')
    #     parameterized_sql = self.bigquery_validator.parameterize_sql('select 2021-07-21')
    #     self.assertEqual(parameterized_sql, 'select {{ ds }}', 'assert_extra_param_exists')
