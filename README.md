### Python BigQuery Validator
Python module for validating BigQuery sql queries with support for Jinja templated variables

This package was built with the goal of automating testing of sql for [Apache Airflow](https://github.com/apache/airflow) dags.


### Build Instructions
Build steps
```python
python3 -m pip install --upgrade build
python3 -m build
```

Upload
```python
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```
