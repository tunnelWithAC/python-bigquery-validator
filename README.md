## Python BigQuery Validator
Python module for validating BigQuery sql queries with support for Jinja templated variables

This package was built with the goal of automating testing of sql for [Apache Airflow](https://github.com/apache/airflow) dags.

Functionality was later added to allow a quick solution for implementing data validation that can be ready as part of a Airflow DAG, Github Action or any other CI/CD process that can run a Python script.

### Installation Instructions
```python
pip install python-bigquery-validator
```


### Validate the output of query results using unit tests
Taken from `bigquery_validator/tests/bigquery_validator_test.py`
```python
class BigqueryResultTest(unittest.TestCase):

    def test_query_executes_by_default(self):
        query = "SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`"

        bqr = BigQueryResult(query)
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
        """
        -- ./sql/bigquery_result_metadata.sql
        SELECT count(*) AS nrows FROM `{{ params.project }}.samples.github_timeline`
        """
        bqr = BigQueryResult(file_path='./sql/bigquery_result_metadata.sql')
        result_metadata = bqr.metadata()
        unique_rows = len(result_metadata['unique_values']['nrows'])
        total_rows = result_metadata['nrows']
        self.assertIsNotNone(result_metadata)
        self.assertEquals(unique_rows, total_rows)

    def test_query_metadata_returns_correct_columns(self):
        query = '''
        select 'andrew' as name, 21 as age
        union all
        select 'james' as name, 20 as age
        '''

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        columns = result_metadata['columns']
        self.assertEquals(columns, ['name', 'age'])
        
    def test_query_metadata_returns_correct_unique_values(self):
        query = '''
        select 'andrew' as name, 21 as age
        union all
        select 'james' as name, 20 as age
        '''

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        unique_names = result_metadata['unique_values']['name']
        self.assertEquals(unique_names, ['andrew', 'james'])

    def test_query_from_file_metadata_returns_correct_unique_values(self):
        """
        -- ./sql/bigquery_result_test.sql
        select 'john' as name, 21 as age
        union all
        select 'peter' as name, 21 as age
        union all
        select 'andrew' as name, 21 as age
        union all
        select 'james' as name, 20 as age
        """
        bqr = BigQueryResult(file_path='./sql/bigquery_result_test.sql')
        result_metadata = bqr.metadata()
        unique_names = result_metadata['unique_values']['name']
        self.assertEquals(unique_names, ['john', 'peter', 'andrew', 'james'])

    def test_query_metadata_returns_correct_null_values(self):
        query = '''
        select 'andrew' as name, null as age
        union all
        select null as name, null as age
        '''

        bqr = BigQueryResult(query)
        result_metadata = bqr.metadata()
        null_names = result_metadata['null_values']['name']
        self.assertEquals(null_names, 1)

        null_age = result_metadata['null_values']['age']
        self.assertEquals(null_age, 2)

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
        self.assertEquals(name_value_counts, {'john': 1, 'andrew': 1})

        age_value_counts = value_counts['age']
        self.assertEquals(age_value_counts, {20: 2})
```


### Validate sql using unit tests

```python
class BigqueryValidatorTest(unittest.TestCase):

    bigquery_validator = BigQueryValidator(return_query_cost_as_dict=True)

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

    def test_query_costs_less_than_1_gb(self):
        query = "SELECT repository_url, repository_has_downloads, repository_created_at, repository_has_issues, " \
                "repository_forks FROM `bigquery-public-data.samples.github_timeline`"
        _, query_cost = self.bigquery_validator.validate_query(query)
        query_cost_gb = query_cost['gb']
        query_cost_mb = query_cost['mb']
        self.assertLess(query_cost_gb, 1, 'assert_query_costs_less_than_1_gigabyte')
        self.assertGreater(query_cost_mb, 100, 'assert_query_costs_greater_than_100_megabyte')
```


### Run functions using the command line
Taken from `bigquery_validator/tests/bigquery_result_test.py`
```python
# Continuously monitor a sql file and automatically validate the sql on every
# saved change to the file
python -m bigquery_validator auto_validate_query_from_file './valid_query.sql'

# Convert the Jinja templated SQL to a valid query
python -m bigquery_validator render_templated_query 'select date("{{ params.date }}") as date'

# Check if query is valid
python -m bigquery_validator validate_query 'select true'

# Check if sql file contains valid query
python -m bigquery_validator validate_query_from_file './valid_query.sql'
```


### Github Actions

An example of how to schedule tests using Github Actions can be found in `.github/workflows/example-validate-query-result.yaml`
