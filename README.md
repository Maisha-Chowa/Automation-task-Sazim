# Playwright Python UI Automation (POM)

Data-driven UI automation framework for a small e-commerce platform using Playwright + Pytest with strict Page Object Model structure.

## Project Structure

- `pages/` -> POM classes and UI actions
- `tests/` -> feature test suites
- `test_data/` -> JSON data sources for data-driven tests
- `reports/` -> runtime outputs (`junit.xml`, `allure-results`, auth state)
- `config.py` -> global settings loaded from `.env`
- `run_all_tests.py` -> one-command runner for full suite or custom pytest args

## Prerequisites

- Python 3.10+ (recommended 3.11)
- `pip`
- Git
- Chrome/Chromium install supported by Playwright

## Setup On Any Device

1. Clone repository

```bash
git clone https://github.com/Maisha-Chowa/Automation-task-Sazim.git
cd Automation-task-Sazim
```

2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
python -m playwright install
```

4. Configure `.env`

Create or update `.env` in project root:

```env
BASE_URL=https://ehsanur-rahman-sazim.github.io/
USERNAME=testuser@teebay.com
PASSWORD=123456
BROWSER=chromium
DEFAULT_TIMEOUT_MS=15000
HEADLESS=false
```

## Running Tests

Run all tests with new runner:

```bash
python run_all_tests.py
```

Run all tests with custom pytest args:

```bash
python run_all_tests.py -k login -q
```

Run all tests directly with pytest:

```bash
pytest tests -q
```

Run a single file:

```bash
pytest tests/test_delete_product.py -q
```

## Allure Report Generation

Pytest is configured to write Allure results to `reports/allure-results`.

1. Execute tests

```bash
python run_all_tests.py
```

2. Generate static report

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

3. Open report locally

```bash
allure open reports/allure-report
```

## Test Plan Summary

- **Login**
  - UI validation
  - Positive and negative authentication scenarios
  - Logout confirm/cancel behavior

- **Registration**
  - UI validation
  - Positive registration flow
  - Field-level and blank-input negative validations

- **Account Settings**
  - UI validation
  - Positive update and persisted value checks
  - Negative validations

- **Add / Update Product**
  - UI validation
  - Positive create and edit flows
  - Dropdown + pricing validations

- **Delete Product**
  - UI validation
  - Positive delete flow with confirmation modal
  - Post-delete verification on `BASE_URL/my-products`

- **Browse Products**
  - Title/category/buy/rent filter combinations
  - Clear/reset handling between test scenarios

- **Buy / Rent Product**
  - Sold/available/owned behavior checks
  - Buy confirm/cancel flows
  - Rent date-range validations
  - Known app issues tracked with `xfail`

## Allure Report Screenshots

![Allure Overview](docs/screenshots/allure-overview.png)
![Allure Suites](docs/screenshots/allure-suites.png)
![Allure Test Details](docs/screenshots/allure-test-details.png)

## How To Capture Allure Report Screenshots

1. Run tests and generate report:
   - `python run_all_tests.py`
   - `allure generate reports/allure-results -o reports/allure-report --clean`
2. Open report:
   - `allure open reports/allure-report`
3. Capture screenshots from:
   - Dashboard/Overview
   - Suites view
   - Individual test details with steps/attachments
4. Save files under `docs/screenshots/` using these exact names:
   - `allure-overview.png`
   - `allure-suites.png`
   - `allure-test-details.png`

## Notes

- Some scenarios are intentionally `xfail` where app behavior is currently inconsistent with expected business rules.
- Use `.env` to switch users/base URL without code changes.

