# Python Version Upgrade Design

**Date:** 2026-04-05
**Status:** Approved

## Goal

Raise the minimum supported Python version from 3.7 to 3.10, add Python 3.11, 3.12, and 3.13 to the CI test matrix, and update `requirements.txt` to current stable package versions.

## Background

The repo currently declares `python_requires='>=3.7'` in `setup.py`. Python 3.7, 3.8, and 3.9 are all end-of-life. The CI test matrix covers 3.7–3.10 in `test-build.yaml` and 3.9/3.12 in `test-python-bigquery-validator.yaml`. The `requirements.txt` is pinned to 2021-era versions.

## Changes

### 1. `setup.py`

- Raise `python_requires` from `>=3.7` to `>=3.10`
- Replace the generic `Programming Language :: Python :: 3` classifier with explicit per-version classifiers:
  - `Programming Language :: Python :: 3.10`
  - `Programming Language :: Python :: 3.11`
  - `Programming Language :: Python :: 3.12`
  - `Programming Language :: Python :: 3.13`

### 2. `.github/workflows/test-build.yaml`

- Remove jobs for Python 3.7, 3.8, 3.9, 3.10
- Add jobs for Python 3.10, 3.11, 3.12, 3.13
- Drop the GCP credentials setup from the old 3.8 job (not relevant to build tests)
- Bump `actions/checkout@v2` → `actions/checkout@v4`

### 3. `.github/workflows/test-python-bigquery-validator.yaml`

- Replace the sequential 3.9 + 3.12 single-job approach with a matrix strategy across 3.10, 3.11, 3.12, 3.13
- Bump `actions/checkout@v2` → `actions/checkout@v4`

### 4. `.github/workflows/publish-to-pypi.yaml`

- Update build Python from 3.12 to 3.13
- Bump `actions/setup-python@v1` → `actions/setup-python@v5`
- Bump `actions/checkout@v2` → `actions/checkout@v4`

### 5. `requirements.txt`

- Update all pinned packages to current stable versions compatible with Python >=3.10
- Retain all existing packages (runtime and dev/publish tools) — splitting into `requirements-dev.txt` is tracked separately in issue #29

## Out of Scope

- Splitting `requirements.txt` into runtime and dev files — tracked in issue #29
- Any code changes to the library itself (no Python 3.10+ syntax changes needed)

## Success Criteria

- `setup.py` declares `python_requires='>=3.10'` with correct PyPI classifiers
- CI passes on Python 3.10, 3.11, 3.12, and 3.13
- `requirements.txt` installs cleanly on all four versions
- Publish workflow builds on Python 3.13
