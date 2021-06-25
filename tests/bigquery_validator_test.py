import unittest

from bigquery_validator import BigQueryValidator


class BigqueryValidatorTest(unittest.TestCase):

    bigquery_validator = BigQueryValidator()

    def test_valid_query_returns_true(self):
        query = "SELECT count(*) FROM `bigquery-public-data.samples.github_timeline`"
        valid_sql = self.bigquery_validator.validate_query(query)
        self.assertTrue(valid_sql)

    def test_bad_query_returns_false(self):
        query = "SELECT count(*) ROM `bigquery-public-data.samples.github_timeline`"
        bad_sql = self.bigquery_validator.validate_query(query)
        self.assertFalse(bad_sql)

    def test_valid_query_from_file_returns_true(self):
        valid_sql = self.bigquery_validator.validate_query_from_file("valid_query.sql")
        self.assertTrue(valid_sql)

    def test_bad_query_from_file_returns_false(self):
        bad_sql = self.bigquery_validator.validate_query_from_file("bad_query.sql")
        self.assertFalse(bad_sql)
