# Playwright UI Automation (POM)

## Buy and Rent Feature Coverage

- Status/tag validation covered for `Available`, `Sold`, and `You Own the product` behavior.
- Action visibility checks:
  - `Available` -> `Buy` and `Rent` buttons visible.
  - `Sold` / owned product -> `Buy` and `Rent` buttons hidden.
- Buy flow covered:
  - Cancel keeps product available.
  - Confirm buy expects sold status and hidden actions.
- Rent flow covered:
  - Modal validation for start/end date inputs.
  - Valid date range and max 1 week scenarios.
  - Invalid date scenarios: past date, same date, end before start, more than 1 week, empty inputs.
  - Cancel keeps product available.
- Some rent validations are marked as `xfail` where app behavior currently does not enforce expected constraints.

## Run Buy/Rent Tests

```bash
pytest tests/test_buy_rent_product.py -q
```

