# Python Version Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Raise the minimum supported Python version from 3.7 to 3.10, expand the CI test matrix to cover 3.10–3.13, and refresh `requirements.txt` to current stable package versions.

**Architecture:** Pure configuration changes — no library code is modified. Changes span `setup.py` (package metadata), five GitHub Actions workflow files (CI/CD), and `requirements.txt` (dependency pins). Each task is independent and can be committed separately.

**Tech Stack:** Python packaging (`setuptools`, `setup.py`), GitHub Actions, pip

---

## File Map

| File | Change |
|------|--------|
| `setup.py` | Raise `python_requires`, update PyPI classifiers |
| `.github/workflows/test-build.yaml` | Replace 3.7/3.8/3.9/3.10 jobs with 3.10/3.11/3.12/3.13 |
| `.github/workflows/test-python-bigquery-validator.yaml` | Convert sequential 3.9+3.12 to matrix across 3.10–3.13 |
| `.github/workflows/test-python-bigquery-result.yaml` | Convert sequential 3.9+3.12 to matrix across 3.10–3.13 |
| `.github/workflows/publish-to-pypi.yaml` | Bump build Python 3.12→3.13, bump actions versions |
| `.github/workflows/example-validate-query-result.yaml` | Bump `actions/checkout@v2` → `@v4` |
| `requirements.txt` | Update all pinned packages to current stable versions |

---

## Task 1: Update `setup.py` package metadata

**Files:**
- Modify: `setup.py`

- [ ] **Step 1: Validate current setup.py syntax**

  ```bash
  python setup.py check
  ```
  Expected: completes without errors.

- [ ] **Step 2: Update `python_requires` and classifiers**

  Replace the `classifiers` list and `python_requires` line in `setup.py`:

  ```python
  classifiers=[
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
      "Programming Language :: Python :: 3.12",
      "Programming Language :: Python :: 3.13",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  packages=setuptools.find_packages(),
  python_requires='>=3.10'
  ```

- [ ] **Step 3: Validate updated setup.py**

  ```bash
  python setup.py check
  ```
  Expected: completes without errors.

- [ ] **Step 4: Commit**

  ```bash
  git add setup.py
  git commit -m "feat: raise minimum Python version to 3.10, update PyPI classifiers"
  ```

---

## Task 2: Update `test-build.yaml`

**Files:**
- Modify: `.github/workflows/test-build.yaml`

- [ ] **Step 1: Replace the entire file contents**

  ```yaml
  name: test-build
  on:
    push
  jobs:
    build-python-3-10:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Set up Python 3.10
          uses: actions/setup-python@v5
          with:
            python-version: '3.10'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
    build-python-3-11:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Set up Python 3.11
          uses: actions/setup-python@v5
          with:
            python-version: '3.11'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
    build-python-3-12:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Set up Python 3.12
          uses: actions/setup-python@v5
          with:
            python-version: '3.12'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
    build-python-3-13:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Set up Python 3.13
          uses: actions/setup-python@v5
          with:
            python-version: '3.13'
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
  ```

- [ ] **Step 2: Validate YAML syntax**

  ```bash
  python -c "import yaml; yaml.safe_load(open('.github/workflows/test-build.yaml'))"
  ```
  Expected: no output (no errors).

- [ ] **Step 3: Commit**

  ```bash
  git add .github/workflows/test-build.yaml
  git commit -m "ci: update test-build matrix to Python 3.10-3.13, drop EOL versions"
  ```

---

## Task 3: Update `test-python-bigquery-validator.yaml`

**Files:**
- Modify: `.github/workflows/test-python-bigquery-validator.yaml`

- [ ] **Step 1: Replace the entire file contents**

  Note: The GCP credentials setup is kept since this workflow runs actual unit tests. The matrix strategy replaces the old sequential job pattern.

  ```yaml
  name: run-bigquery-validator-unit-tests
  on:
    push
  jobs:
    bigquery-validator-unit-tests:
      runs-on: ubuntu-latest
      strategy:
        matrix:
          python-version: ['3.10', '3.11', '3.12', '3.13']
      steps:
      - uses: actions/checkout@v4
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v0
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          export_default_credentials: true
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
      - name: Run unit tests
        run: |
          cd bigquery_validator/tests
          pytest bigquery_validator_test.py
  ```

- [ ] **Step 2: Validate YAML syntax**

  ```bash
  python -c "import yaml; yaml.safe_load(open('.github/workflows/test-python-bigquery-validator.yaml'))"
  ```
  Expected: no output (no errors).

- [ ] **Step 3: Commit**

  ```bash
  git add .github/workflows/test-python-bigquery-validator.yaml
  git commit -m "ci: convert bigquery-validator tests to matrix strategy for Python 3.10-3.13"
  ```

---

## Task 4: Update `test-python-bigquery-result.yaml`

**Files:**
- Modify: `.github/workflows/test-python-bigquery-result.yaml`

- [ ] **Step 1: Replace the entire file contents**

  ```yaml
  name: run-bigquery-result-unit-tests
  on:
    push
  jobs:
    bigquery-result-unit-tests:
      runs-on: ubuntu-latest
      strategy:
        matrix:
          python-version: ['3.10', '3.11', '3.12', '3.13']
      steps:
      - uses: actions/checkout@v4
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v0
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          export_default_credentials: true
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest coverage
      - name: Run unit tests
        run: |
          cd bigquery_validator/tests
          pytest bigquery_result_test.py
  ```

- [ ] **Step 2: Validate YAML syntax**

  ```bash
  python -c "import yaml; yaml.safe_load(open('.github/workflows/test-python-bigquery-result.yaml'))"
  ```
  Expected: no output (no errors).

- [ ] **Step 3: Commit**

  ```bash
  git add .github/workflows/test-python-bigquery-result.yaml
  git commit -m "ci: convert bigquery-result tests to matrix strategy for Python 3.10-3.13"
  ```

---

## Task 5: Update `publish-to-pypi.yaml`

**Files:**
- Modify: `.github/workflows/publish-to-pypi.yaml`

- [ ] **Step 1: Replace the entire file contents**

  Changes: `ubuntu-18.04` → `ubuntu-latest`, Python `3.12` → `3.13`, `setup-python@v1` → `@v5`, `checkout@v2` → `@v4`.

  ```yaml
  name: publish-to-pypi
  on:
    push:
      tags: [ publish-pypi-* ]
  jobs:
    build-and-publish:
      name: Build and publish package to PyPI and TestPyPI
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Set up Python 3.13
          uses: actions/setup-python@v5
          with:
            python-version: '3.13'
        - name: Install pypa/build
          run: >-
            python -m
            pip install
            build
            --user
        - name: Build a binary wheel and a source tarball
          run: >-
            python -m
            build
            --sdist
            --wheel
            --outdir dist/
            .
        - name: Publish distribution package to Test PyPI
          uses: pypa/gh-action-pypi-publish@master
          with:
            password: ${{ secrets.PYPI_TEST_API_KEY }}
            repository_url: https://test.pypi.org/legacy/
        - name: Publish distribution to PyPI
          uses: pypa/gh-action-pypi-publish@master
          with:
            password: ${{ secrets.PYPI_API_KEY }}
  ```

- [ ] **Step 2: Validate YAML syntax**

  ```bash
  python -c "import yaml; yaml.safe_load(open('.github/workflows/publish-to-pypi.yaml'))"
  ```
  Expected: no output (no errors).

- [ ] **Step 3: Commit**

  ```bash
  git add .github/workflows/publish-to-pypi.yaml
  git commit -m "ci: build and publish using Python 3.13, bump actions to latest versions"
  ```

---

## Task 6: Update `example-validate-query-result.yaml`

**Files:**
- Modify: `.github/workflows/example-validate-query-result.yaml`

- [ ] **Step 1: Bump `actions/checkout@v2` to `@v4`**

  Replace line 14:
  ```yaml
        - uses: actions/checkout@v4
  ```

- [ ] **Step 2: Validate YAML syntax**

  ```bash
  python -c "import yaml; yaml.safe_load(open('.github/workflows/example-validate-query-result.yaml'))"
  ```
  Expected: no output (no errors).

- [ ] **Step 3: Commit**

  ```bash
  git add .github/workflows/example-validate-query-result.yaml
  git commit -m "ci: bump actions/checkout to v4"
  ```

---

## Task 7: Update `requirements.txt` to current stable versions

**Files:**
- Modify: `requirements.txt`

This task generates updated pins by installing unpinned packages into a fresh Python 3.10 environment and freezing the result.

- [ ] **Step 1: Create a temp requirements file without pins**

  ```bash
  sed 's/==.*//' requirements.txt > /tmp/requirements-unpinned.txt
  cat /tmp/requirements-unpinned.txt
  ```
  Expected: same package list, no version numbers.

- [ ] **Step 2: Create a fresh virtualenv with Python 3.10 and install**

  > **Note if running on macOS:** `SecretStorage` and `jeepney` are Linux-only packages that won't install or freeze correctly on macOS. Either run this step inside a Linux Docker container (`docker run --rm -it -v $(pwd):/work python:3.10-slim bash`) or manually look up the current versions of those two packages on PyPI and add them by hand after the freeze step.

  ```bash
  python3.10 -m venv /tmp/req-update-env
  source /tmp/req-update-env/bin/activate
  pip install --upgrade pip
  pip install -r /tmp/requirements-unpinned.txt
  ```
  Expected: all packages install without errors. If any package fails, note the error — it may indicate a package incompatible with Python 3.10 that needs manual attention.

- [ ] **Step 3: Freeze the installed versions**

  ```bash
  pip freeze > /tmp/new-requirements.txt
  cat /tmp/new-requirements.txt
  deactivate
  ```
  Expected: a fully-pinned list of packages and their transitive dependencies.

- [ ] **Step 4: Extract only the packages currently in `requirements.txt`**

  The freeze output includes transitive deps not in the original file. Filter it to match only the packages already listed:

  ```bash
  # Extract package names from original requirements.txt (strip versions and extras)
  grep -v '^#' requirements.txt | sed 's/[>=<!\[].*//' | tr '[:upper:]' '[:lower:]' | sort > /tmp/orig-pkgs.txt

  # Extract matching lines from the frozen output
  while IFS= read -r pkg; do
    grep -i "^${pkg}==" /tmp/new-requirements.txt
  done < /tmp/orig-pkgs.txt
  ```
  Expected: one pinned line per package in the original `requirements.txt`.

- [ ] **Step 5: Replace `requirements.txt` with the updated pins**

  Using the output from Step 4, replace `requirements.txt`. Keep the same package order as the original file for readability. Packages that were unpinned in the original (e.g. `google-cloud-bigquery`, `numpy`, `pandas`, `protobuf`) should remain unpinned.

- [ ] **Step 6: Verify the updated requirements install cleanly on Python 3.10**

  ```bash
  python3.10 -m venv /tmp/verify-env
  source /tmp/verify-env/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  deactivate
  ```
  Expected: all packages install without errors or conflicts.

- [ ] **Step 7: Commit**

  ```bash
  git add requirements.txt
  git commit -m "chore: update requirements.txt to current stable package versions"
  ```

---

## Final Step: Open PR

- [ ] **Push the branch and open a PR**

  ```bash
  git push origin <branch-name>
  gh pr create --title "feat: upgrade Python support to 3.10-3.13" --body "Implements the design spec in docs/superpowers/specs/2026-04-05-python-version-upgrade-design.md

  - Raises minimum Python version from 3.7 to 3.10
  - Expands CI test matrix to Python 3.10, 3.11, 3.12, 3.13
  - Converts sequential test jobs to matrix strategy
  - Updates publish workflow to build on Python 3.13
  - Refreshes requirements.txt to current stable versions
  - Bumps all GitHub Actions to latest versions

  Closes #29 is tracked separately (requirements-dev.txt split)"
  ```
