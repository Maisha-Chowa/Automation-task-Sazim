import json
from pathlib import Path

import pytest

from config import Settings
from pages.account_settings_page import AccountSettingsPage


def _load_account_settings_data() -> dict:
    data_path = Path(__file__).resolve().parent.parent / "test_data" / "account_settings.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


ACCOUNT_SETTINGS_DATA = _load_account_settings_data()


@pytest.mark.parametrize("case", ACCOUNT_SETTINGS_DATA["ui_validations"], ids=lambda c: c["name"])
def test_account_settings_ui_validation(authenticated_page, case: dict) -> None:
    account_settings_page = AccountSettingsPage(authenticated_page)
    account_settings_page.open_from_my_products()

    assert account_settings_page.is_on_account_settings_page()
    assert account_settings_page.text_visible(account_settings_page.PAGE_HEADING_TEXT)
    assert authenticated_page.locator(account_settings_page.FIRST_NAME_INPUT).is_visible()
    assert authenticated_page.locator(account_settings_page.LAST_NAME_INPUT).is_visible()
    assert authenticated_page.locator(account_settings_page.ADDRESS_INPUT).is_visible()
    assert authenticated_page.locator(account_settings_page.EMAIL_INPUT).is_visible()
    assert authenticated_page.locator(account_settings_page.PHONE_NUMBER_INPUT).is_visible()
    assert authenticated_page.locator(account_settings_page.UPDATE_BUTTON).is_visible()


@pytest.mark.parametrize("case", ACCOUNT_SETTINGS_DATA["positive_cases"], ids=lambda c: c["name"])
def test_update_account_settings_positive(authenticated_page, case: dict) -> None:
    account_settings_page = AccountSettingsPage(authenticated_page)
    account_settings_page.open_from_my_products()
    account_settings_page.update_account(
        first_name=case["first_name"],
        last_name=case["last_name"],
        address=case["address"],
        email=case["email"],
        phone_number=case["phone_number"],
    )

    assert authenticated_page.url == Settings.ACCOUNT_SETTINGS_URL

    # Required validation flow: return to my-products, then open account settings and verify persisted data.
    account_settings_page.go_to_my_products()
    account_settings_page.open_from_my_products()
    actual_values = account_settings_page.current_form_values()

    assert actual_values["first_name"] == case["first_name"]
    assert actual_values["last_name"] == case["last_name"]
    assert actual_values["address"] == case["address"]
    assert actual_values["email"] == case["email"]
    assert actual_values["phone_number"].lstrip("0") == case["phone_number"].lstrip("0")


@pytest.mark.parametrize("case", ACCOUNT_SETTINGS_DATA["negative_cases"], ids=lambda c: c["name"])
def test_update_account_settings_negative(authenticated_page, case: dict) -> None:
    account_settings_page = AccountSettingsPage(authenticated_page)
    account_settings_page.open_from_my_products()
    account_settings_page.update_account(
        first_name=case["first_name"],
        last_name=case["last_name"],
        address=case["address"],
        email=case["email"],
        phone_number=case["phone_number"],
    )

    if "expected_messages" in case:
        for expected_message in case["expected_messages"]:
            assert account_settings_page.text_visible(expected_message)
    else:
        assert account_settings_page.text_visible(case["expected_message"])

