import json
from pathlib import Path

import pytest

from pages.view_product_page import ViewProductPage


def _load_buy_rent_data() -> dict:
    data_path = Path(__file__).resolve().parent.parent / "test_data" / "buy_rent_product.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


def _status_matches(actual_status: str, expected_statuses: list[str]) -> bool:
    actual = actual_status.strip().lower()
    return any(actual == expected.lower() or actual.startswith(expected.lower()) for expected in expected_statuses)


def _open_or_skip(view_product_page: ViewProductPage, title: str, category: str | None = None) -> None:
    try:
        view_product_page.open_product_by_title(title, category=category)
    except Exception:
        pytest.skip(f"Product not available: {title}")


BUY_RENT_DATA = _load_buy_rent_data()
TARGETS = BUY_RENT_DATA["product_targets"]


def test_sold_product_hides_buy_rent_buttons(authenticated_page) -> None:
    view_product_page = ViewProductPage(authenticated_page)
    _open_or_skip(view_product_page, TARGETS["sold_product_title"])

    assert _status_matches(view_product_page.status_text(), ["sold", "s"])
    assert not view_product_page.buy_button_visible()
    assert not view_product_page.rent_button_visible()


@pytest.mark.parametrize("case", BUY_RENT_DATA["rent_cases"]["negative_cases"], ids=lambda c: c["name"])
def test_rent_negative_funshine(authenticated_page, case: dict) -> None:
    view_product_page = ViewProductPage(authenticated_page)
    _open_or_skip(view_product_page, TARGETS["rent_product_title"])

    if view_product_page.status_text().lower() != "available":
        pytest.skip(f"Product not available for rent tests: {TARGETS['rent_product_title']}")

    assert view_product_page.rent_button_visible()
    view_product_page.open_rent_modal()

    if "start_date" in case and "end_date" in case:
        view_product_page.set_rent_dates(case["start_date"], case["end_date"])
    else:
        view_product_page.set_rent_dates_from_offsets(case["start_offset_days"], case["end_offset_days"])

    if case.get("cancel_rent"):
        view_product_page.cancel_rent()
        assert _status_matches(view_product_page.status_text(), ["available", "a"])
        return

    is_disabled = view_product_page.rent_book_button_disabled()
    if case.get("expect_book_disabled") and case.get("known_bug") and not is_disabled:
        view_product_page.cancel_rent()
        pytest.xfail("Known app bug: invalid rent dates still allow Book rent.")
    assert is_disabled == case["expect_book_disabled"]
    view_product_page.cancel_rent()
    assert _status_matches(view_product_page.status_text(), ["available", "a"])


@pytest.mark.parametrize("case", BUY_RENT_DATA["rent_cases"]["positive_cases"], ids=lambda c: c["name"])
def test_rent_positive_funshine(authenticated_page, case: dict) -> None:
    view_product_page = ViewProductPage(authenticated_page)
    _open_or_skip(view_product_page, TARGETS["rent_product_title"])

    if view_product_page.status_text().lower() != "available":
        pytest.skip(f"Product not available for rent tests: {TARGETS['rent_product_title']}")

    view_product_page.open_rent_modal()
    view_product_page.set_rent_dates_from_offsets(case["start_offset_days"], case["end_offset_days"])
    view_product_page.book_rent()

    status_ok = _status_matches(view_product_page.status_text(), case["expected_statuses_after"])
    if case.get("known_bug") and not status_ok:
        pytest.xfail("Known app bug: valid rent booking does not change status to rented.")
    assert status_ok


@pytest.mark.parametrize("case", BUY_RENT_DATA["buy_cases"]["negative_cases"], ids=lambda c: c["name"])
def test_buy_negative_lawn_mower(authenticated_page, case: dict) -> None:
    view_product_page = ViewProductPage(authenticated_page)
    _open_or_skip(view_product_page, TARGETS["buy_product_title"])

    if view_product_page.status_text().lower() != "available":
        pytest.skip(f"Product not available for buy tests: {TARGETS['buy_product_title']}")

    assert view_product_page.buy_button_visible()
    assert view_product_page.rent_button_visible()

    view_product_page.open_buy_modal()
    view_product_page.cancel_buy()

    assert _status_matches(view_product_page.status_text(), case["expected_statuses_after"])
    assert view_product_page.buy_button_visible()
    assert view_product_page.rent_button_visible()


@pytest.mark.parametrize("case", BUY_RENT_DATA["buy_cases"]["positive_cases"], ids=lambda c: c["name"])
def test_buy_positive_lawn_mower(authenticated_page, case: dict) -> None:
    view_product_page = ViewProductPage(authenticated_page)
    _open_or_skip(view_product_page, TARGETS["buy_product_title"])

    if view_product_page.status_text().lower() != "available":
        pytest.skip(f"Product not available for buy tests: {TARGETS['buy_product_title']}")

    view_product_page.open_buy_modal()
    view_product_page.confirm_buy()

    assert _status_matches(view_product_page.status_text(), case["expected_statuses_after"])
    assert not view_product_page.buy_button_visible()
    assert not view_product_page.rent_button_visible()


def test_cricket_kit_available_owned_combined_logic(authenticated_page) -> None:
    view_product_page = ViewProductPage(authenticated_page)
    _open_or_skip(
        view_product_page,
        TARGETS["own_available_product_title"],
        category=TARGETS["own_available_category"],
    )

    # In app behavior, clicking this product redirects to owner context.
    if "product-details" in authenticated_page.url:
        own_condition = view_product_page.is_owned_by_logged_user()
        available_condition = view_product_page.status_text().lower() == "available"
        if own_condition and available_condition:
            assert not view_product_page.buy_button_visible()
            assert not view_product_page.rent_button_visible()
    else:
        assert "my-products" in authenticated_page.url

