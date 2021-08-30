import unittest

from bigquery_validator.bigquery_validator import BigQueryValidator


class BigqueryValidatorTest(unittest.TestCase):

    bigquery_validator = BigQueryValidator()

    def test_valid_query_returns_true(self):
        query = "SELECT count(*) FROM `{{ params.project }}.samples.github_timeline`"
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

    def test_parameterised_query_is_formatted_correctly(self):
        templated_query = "select count(*) from `{{ params.project }}.samples.github_timeline`"
        rendered_query = self.bigquery_validator.render_templated_query(templated_query)
        self.assertEquals(rendered_query, 'select count(*) from `bigquery-public-data.samples.github_timeline`')

    def test_parameterised_query_from_file_is_formatted_correctly(self):
        rendered_query = self.bigquery_validator.render_templated_query_from_file("./valid_query.sql")
        self.assertEquals(rendered_query, 'select count(*) from `bigquery-public-data.samples.github_timeline`')

    def test_extra_params_are_loaded_from_file(self):
        test_param = self.bigquery_validator.params.get('environment')
        self.assertEqual(test_param, 'test', 'assert_extra_param_exists')

    # Test expected query size
