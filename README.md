### Python BigQuery Validator
Python module for validating BigQuery sql queries with support for Jinja templated variables

This package was built with the goal of automating testing of sql for [Apache Airflow](https://github.com/apache/airflow) dags.

```python
pip install python-bigquery-validator==0.0.1a3
```

python -m bigquery_validator dry_run_query 'select true'

```python
python -m bigquery_validator -f dry_run_query -p 'select true'
render_templated_query 'select date("{{ params.date }}") as date'
validate_query 'select true'
validate_query_from_file './valid_query.sql'
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
