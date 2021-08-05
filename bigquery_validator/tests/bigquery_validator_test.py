import os
import unittest

from bigquery_validator.bigquery_validator import BigQueryValidator


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
        local_config_path = './bq_validator_config.json'
        if os.path.isfile(local_config_path):
            try:
                f = open(local_config_path, "r")
                local_config_file_content = f.read()
                import json
                local_config_params = json.loads(local_config_file_content)
                print(local_config_params)
            except Exception as e:
                print(e)
        test_param = self.bigquery_validator.params.get('environment')
        self.assertEqual(test_param, 'test', 'assert_extra_param_exists')

    # Test expected query size
