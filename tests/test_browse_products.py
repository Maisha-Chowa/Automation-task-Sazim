import json
from pathlib import Path

import pytest

from pages.browse_products_page import BrowseProductsPage


def _load_browse_products_data() -> dict:
    data_path = Path(__file__).resolve().parent.parent / "test_data" / "browse_products.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


def _contains_expected_titles(actual_titles: list[str], expected_titles: list[str]) -> bool:
    return all(
        any(expected_title.lower() in actual_title.lower() for actual_title in actual_titles)
        for expected_title in expected_titles
    )


BROWSE_DATA = _load_browse_products_data()


@pytest.mark.parametrize("case", BROWSE_DATA["ui_validations"], ids=lambda c: c["name"])
def test_browse_products_ui_validation(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()

    assert browse_page.is_on_browse_products_page()
    assert authenticated_page.locator(browse_page.TITLE_INPUT).is_visible()
    assert authenticated_page.locator(browse_page.CATEGORY_DROPDOWN).is_visible()
    assert authenticated_page.locator(browse_page.BUY_FILTER_CHECKBOX).count() > 0
    assert authenticated_page.locator(browse_page.RENT_FILTER_CHECKBOX).count() > 0
    assert authenticated_page.get_by_role("button", name=browse_page.CLEAR_BUTTON_TEXT).is_visible()
    assert authenticated_page.get_by_role("button", name=browse_page.FILTER_BUTTON_TEXT).is_visible()

    browse_page.enable_buy_filter()
    assert authenticated_page.locator(browse_page.MIN_BUY_RANGE_INPUT).is_visible()
    assert authenticated_page.locator(browse_page.MAX_BUY_RANGE_INPUT).is_visible()
    browse_page.clear_filters()

    browse_page.enable_rent_filter()
    assert authenticated_page.locator(browse_page.MIN_RENT_RANGE_INPUT).is_visible()
    assert authenticated_page.locator(browse_page.MAX_RENT_RANGE_INPUT).is_visible()
    assert authenticated_page.locator(browse_page.RENT_DURATION_DROPDOWN).is_visible()
    browse_page.clear_filters()


@pytest.mark.parametrize("case", BROWSE_DATA["title_filter"]["positive_cases"], ids=lambda c: c["name"])
def test_browse_products_title_filter_positive(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()
    browse_page.clear_filters()

    try:
        browse_page.fill_title(case["title"])
        browse_page.apply_filters()
        actual_titles = browse_page.product_titles()
        condition = _contains_expected_titles(actual_titles, case["expected_titles"]) and all(
            case["title"].lower() in actual_title.lower()
            for actual_title in actual_titles
        )

        if case.get("known_bug") and not condition:
            pytest.xfail("Known app bug: title filter is not applied.")

        assert condition
    finally:
        browse_page.clear_filters()


@pytest.mark.parametrize("case", BROWSE_DATA["title_filter"]["negative_cases"], ids=lambda c: c["name"])
def test_browse_products_title_filter_negative(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()
    browse_page.clear_filters()

    try:
        browse_page.fill_title(case["title"])
        browse_page.apply_filters()
        actual_count = browse_page.product_count()
        condition = actual_count == case["expected_count"]

        if case.get("known_bug") and not condition:
            pytest.xfail("Known app bug: title filter is not applied.")

        assert condition
    finally:
        browse_page.clear_filters()


@pytest.mark.parametrize("case", BROWSE_DATA["category_filter"]["positive_cases"], ids=lambda c: c["name"])
def test_browse_products_category_filter_positive(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()
    browse_page.clear_filters()

    try:
        browse_page.choose_category(case["category"])
        browse_page.apply_filters()
        assert _contains_expected_titles(browse_page.product_titles(), case["expected_titles"])
    finally:
        browse_page.clear_filters()


@pytest.mark.parametrize("case", BROWSE_DATA["category_filter"]["negative_cases"], ids=lambda c: c["name"])
def test_browse_products_category_filter_negative(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()
    browse_page.clear_filters()

    try:
        browse_page.choose_category(case["category"])
        browse_page.apply_filters()
        titles = browse_page.product_titles()
        if "expected_count" in case:
            assert len(titles) == case["expected_count"]
        if "unexpected_titles" in case:
            assert all(
                all(unexpected.lower() not in title.lower() for title in titles)
                for unexpected in case["unexpected_titles"]
            )
    finally:
        browse_page.clear_filters()


@pytest.mark.parametrize("case", BROWSE_DATA["buy_filter"]["positive_cases"], ids=lambda c: c["name"])
def test_browse_products_buy_filter_positive(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()
    browse_page.clear_filters()

    try:
        browse_page.set_buy_range(case["min_buy_range"], case["max_buy_range"])
        browse_page.apply_filters()
        assert _contains_expected_titles(browse_page.product_titles(), case["expected_titles"])
    finally:
        browse_page.clear_filters()


@pytest.mark.parametrize("case", BROWSE_DATA["buy_filter"]["negative_cases"], ids=lambda c: c["name"])
def test_browse_products_buy_filter_negative(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()
    browse_page.clear_filters()

    try:
        browse_page.set_buy_range(case["min_buy_range"], case["max_buy_range"])
        browse_page.apply_filters()
        assert browse_page.product_count() == case["expected_count"]
    finally:
        browse_page.clear_filters()


@pytest.mark.parametrize("case", BROWSE_DATA["rent_filter"]["positive_cases"], ids=lambda c: c["name"])
def test_browse_products_rent_filter_positive(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()
    browse_page.clear_filters()

    try:
        browse_page.set_rent_range(case["min_rent_range"], case["max_rent_range"], case["rent_duration_type"])
        browse_page.apply_filters()
        assert _contains_expected_titles(browse_page.product_titles(), case["expected_titles"])
    finally:
        browse_page.clear_filters()


@pytest.mark.parametrize("case", BROWSE_DATA["rent_filter"]["negative_cases"], ids=lambda c: c["name"])
def test_browse_products_rent_filter_negative(authenticated_page, case: dict) -> None:
    browse_page = BrowseProductsPage(authenticated_page)
    browse_page.open_from_my_products()
    browse_page.clear_filters()

    try:
        browse_page.set_rent_range(case["min_rent_range"], case["max_rent_range"], case["rent_duration_type"])
        browse_page.apply_filters()
        assert browse_page.product_count() == case["expected_count"]
    finally:
        browse_page.clear_filters()

