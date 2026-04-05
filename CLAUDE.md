# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python package (`python-bigquery-validator` on PyPI) for validating BigQuery SQL queries with Jinja2 templated variable support. Designed for use in CI/CD pipelines and Apache Airflow DAG testing.

## Commands

### Install dependencies
```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Run tests
```bash
# All tests (requires GCP credentials)
pytest bigquery_validator/tests/

# Single test file
pytest bigquery_validator/tests/bigquery_validator_test.py

# Single test
pytest bigquery_validator/tests/bigquery_validator_test.py::BigqueryValidatorTest::test_valid_query_returns_true

# With coverage
coverage run -m pytest bigquery_validator/tests/
coverage report -m
coverage json --fail-under=80
```

### Build the package
```bash
python -m build --sdist --wheel --outdir dist/
```

## Architecture

### Core Classes

**`bigquery_validator/bigquery_validator.py` — `BigQueryValidator`**
- Primary class for query validation and cost estimation
- Renders Jinja2 templates via `render_templated_query()` before sending to BigQuery
- `validate_query()` returns `(bool, message_or_cost_dict)` tuple
- `dry_run_query()` estimates query cost without executing
- `auto_validate_query_from_file()` monitors a `.sql` file for changes and re-validates

**`bigquery_validator/bigquery_result.py` — `BigQueryResult`**
- Executes queries and extracts metadata (column names, null counts, unique values, value distributions)
- Takes a `BigQueryValidator` instance as a dependency
- Batches large result sets to prevent memory overflow
- `metadata()` returns a dict with `columns`, `nrows`, `ncols`, `null_values`, `unique_values`, `value_counts`

**`bigquery_validator/bigquery_validator_util.py`**
- `get_default_params()` — returns Airflow-like date params (`ds`, `tomorrow_ds`, etc.)
- `read_sql_file()` — reads SQL from file, stripping leading comment lines
- Terminal color helpers (`print_success`, `print_failure`)

### Parameter / Config Loading

Parameters for Jinja2 template rendering are loaded in priority order (lowest to highest):

1. Hardcoded defaults in `get_default_params()` (Airflow-style date variables)
2. `~/.python_bigquery_validator/config.json` (global user config)
3. `./bq_validator_config.json` (local project config)
4. Constructor `params` argument

Templates use `{{ params.key }}` syntax, mirroring Apache Airflow's Jinja context.

### GCP Authentication

Tests and the validator both require a GCP project and service account credentials. In CI, `GCP_PROJECT_ID` and `GCP_SA_KEY` are passed as GitHub Actions secrets and activated via `gcloud auth activate-service-account`.

### Publishing to PyPI

Publishing is triggered by pushing a tag matching `publish-pypi-*`. The workflow builds wheel + sdist and publishes to TestPyPI then PyPI using `PYPI_TEST_API_KEY` and `PYPI_API_KEY` secrets.
