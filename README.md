### Python BigQuery Validator
Python module for validating BigQuery sql queries with support for Jinja templated variables

This package was built with the goal of automating testing of sql for [Apache Airflow](https://github.com/apache/airflow) dags.

### Installation Instructions
```python
pip install python-bigquery-validator
```

### Validate sql using unit tests

```python
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
        valid_sql = self.bigquery_validator.validate_query_from_file("./valid_query.sql")
        self.assertTrue(valid_sql)

    def test_bad_query_from_file_returns_false(self):
        bad_sql = self.bigquery_validator.validate_query_from_file("./bad_query.sql")
        self.assertFalse(bad_sql, 'assert_bad_sql_from_file_fails_validation')
```

### Run functions using the command line
```python
python -m bigquery_validator dry_run_query 'select true'
```

```python
python -m bigquery_validator render_templated_query 'select date("{{ params.date }}") as date'
```


```python
python -m bigquery_validator validate_query 'select true'
```

```python
python -m bigquery_validator validate_query_from_file './valid_query.sql'
```

### Build Instructions
Build steps
```python
python3 -m pip install --upgrade build
python3 -m build
```

Upload
```python
python3 -m pip install --upgrade twine
python3 -m twine upload --repository pypi dist/*
```
