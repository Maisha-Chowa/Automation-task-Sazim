import json
import time
from pathlib import Path

import pytest

from config import Settings
from pages.add_update_product_page import AddUpdateProductPage


def _load_add_product_data() -> dict:
    data_path = Path(__file__).resolve().parent.parent / "test_data" / "add_update_product.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


def _unique_title(base_title: str) -> str:
    return f"{base_title} {int(time.time() * 1000)}"


ADD_PRODUCT_DATA = _load_add_product_data()


@pytest.mark.parametrize("case", ADD_PRODUCT_DATA["ui_validations"], ids=lambda c: c["name"])
def test_add_product_ui_validation(authenticated_page, case: dict) -> None:
    add_product_page = AddUpdateProductPage(authenticated_page)
    add_product_page.open_from_my_products()

    assert add_product_page.is_on_add_product_page()
    assert add_product_page.text_visible(add_product_page.PAGE_HEADING_TEXT)
    assert authenticated_page.locator(add_product_page.TITLE_INPUT).is_visible()
    assert authenticated_page.locator(add_product_page.DESCRIPTION_INPUT).is_visible()
    assert authenticated_page.locator(add_product_page.PURCHASE_PRICE_INPUT).is_visible()
    assert authenticated_page.locator(add_product_page.RENT_PRICE_INPUT).is_visible()
    assert authenticated_page.locator(add_product_page.CATEGORIES_DROPDOWN).is_visible()
    assert authenticated_page.locator(add_product_page.RENT_DURATION_DROPDOWN).is_visible()
    assert authenticated_page.locator(add_product_page.SUBMIT_BUTTON).is_visible()


@pytest.mark.parametrize("case", ADD_PRODUCT_DATA["positive_cases"], ids=lambda c: c["name"])
def test_add_product_positive(authenticated_page, case: dict) -> None:
    add_product_page = AddUpdateProductPage(authenticated_page)
    add_product_page.open_from_my_products()

    title = _unique_title(case["title"]) if case.get("use_unique_title") else case["title"]
    add_product_page.submit_product(
        title=title,
        description=case["description"],
        purchase_price=case["purchase_price"],
        rent_price=case["rent_price"],
        category=case["category"],
        rent_duration_type=case["rent_duration_type"],
    )

    assert authenticated_page.url == Settings.MY_PRODUCTS_URL
    assert add_product_page.product_visible_on_my_products(title)


@pytest.mark.parametrize("case", ADD_PRODUCT_DATA["negative_cases"], ids=lambda c: c["name"])
def test_add_product_negative(authenticated_page, case: dict) -> None:
    add_product_page = AddUpdateProductPage(authenticated_page)
    add_product_page.open_from_my_products()

    add_product_page.fill_form(
        title=case["title"],
        description=case["description"],
        purchase_price=case["purchase_price"],
        rent_price=case["rent_price"],
    )
    if case["category"]:
        add_product_page.choose_category(case["category"])
    if case["rent_duration_type"]:
        add_product_page.choose_rent_duration(case["rent_duration_type"])
    add_product_page.submit()

    if "expected_any_groups" in case:
        for expected_group in case["expected_any_groups"]:
            assert any(add_product_page.text_visible(message) for message in expected_group)
    elif "expected_messages" in case:
        for expected_message in case["expected_messages"]:
            assert add_product_page.text_visible(expected_message)
    else:
        assert add_product_page.text_visible(case["expected_message"])


@pytest.mark.parametrize("case", ADD_PRODUCT_DATA["update_ui_validations"], ids=lambda c: c["name"])
def test_update_product_ui_validation(authenticated_page, case: dict) -> None:
    add_product_page = AddUpdateProductPage(authenticated_page)
    add_product_page.go_to_my_products()
    add_product_page.open_existing_product_for_update(case["search_title_from_add_positive"])

    assert add_product_page.is_on_edit_product_page()
    assert add_product_page.text_visible(add_product_page.EDIT_PAGE_HEADING_TEXT)
    assert authenticated_page.locator(add_product_page.TITLE_INPUT).is_visible()
    assert authenticated_page.locator(add_product_page.DESCRIPTION_INPUT).is_visible()
    assert authenticated_page.locator(add_product_page.PURCHASE_PRICE_INPUT).is_visible()
    assert authenticated_page.locator(add_product_page.RENT_PRICE_INPUT).is_visible()
    assert authenticated_page.locator(add_product_page.CATEGORIES_DROPDOWN).is_visible()
    assert authenticated_page.locator(add_product_page.RENT_DURATION_DROPDOWN).is_visible()
    assert authenticated_page.locator(add_product_page.SUBMIT_BUTTON).is_visible()


@pytest.mark.parametrize("case", ADD_PRODUCT_DATA["update_positive_cases"], ids=lambda c: c["name"])
def test_update_product_positive(authenticated_page, case: dict) -> None:
    add_product_page = AddUpdateProductPage(authenticated_page)
    add_product_page.go_to_my_products()
    add_product_page.open_existing_product_for_update(case["search_title_from_add_positive"])

    updated_title = _unique_title(case["updated_title"]) if case.get("use_unique_title") else case["updated_title"]
    add_product_page.fill_form(
        title=updated_title,
        description=case["updated_description"],
        purchase_price=case["updated_purchase_price"],
        rent_price=case["updated_rent_price"],
    )
    add_product_page.choose_category(case["updated_category"])
    add_product_page.choose_rent_duration(case["updated_rent_duration_type"])
    add_product_page.submit()

    # App currently stays on edit page after update, so navigate via navbar for verification.
    add_product_page.go_to_my_products()
    assert authenticated_page.url == Settings.MY_PRODUCTS_URL
    assert add_product_page.product_visible_on_my_products(updated_title)


@pytest.mark.parametrize("case", ADD_PRODUCT_DATA["update_negative_cases"], ids=lambda c: c["name"])
def test_update_product_negative(authenticated_page, case: dict) -> None:
    add_product_page = AddUpdateProductPage(authenticated_page)
    add_product_page.go_to_my_products()
    add_product_page.open_existing_product_for_update(case["search_title_from_add_positive"])

    add_product_page.fill_form(
        title=case["title"],
        description=case["description"],
        purchase_price=case["purchase_price"],
        rent_price=case["rent_price"],
    )
    add_product_page.submit()

    if "expected_any_groups" in case:
        for expected_group in case["expected_any_groups"]:
            assert any(add_product_page.text_visible(message) for message in expected_group)
    elif "expected_messages" in case:
        for expected_message in case["expected_messages"]:
            assert add_product_page.text_visible(expected_message)
    else:
        assert add_product_page.text_visible(case["expected_message"])

