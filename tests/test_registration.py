import json
from pathlib import Path

import pytest

from config import Settings
from pages.registration_page import RegistrationPage


def _load_registration_data() -> dict:
    data_path = Path(__file__).resolve().parent.parent / "test_data" / "registration.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


REGISTRATION_DATA = _load_registration_data()


@pytest.mark.parametrize("case", REGISTRATION_DATA["ui_validations"], ids=lambda c: c["name"])
def test_registration_ui_validation(page, case: dict) -> None:
    registration_page = RegistrationPage(page)
    registration_page.open_from_login()

    assert registration_page.is_on_registration_page()
    assert registration_page.text_visible(registration_page.PAGE_HEADING_TEXT)
    assert page.locator(registration_page.FIRST_NAME_INPUT).is_visible()
    assert page.locator(registration_page.LAST_NAME_INPUT).is_visible()
    assert page.locator(registration_page.ADDRESS_INPUT).is_visible()
    assert page.locator(registration_page.EMAIL_INPUT).is_visible()
    assert page.locator(registration_page.PHONE_NUMBER_INPUT).is_visible()
    assert page.locator(registration_page.PASSWORD_INPUT).is_visible()
    assert page.locator(registration_page.CONFIRM_PASSWORD_INPUT).is_visible()
    assert page.locator(registration_page.REGISTER_BUTTON).is_visible()
    assert page.locator(registration_page.SIGN_IN_LINK).is_visible()


@pytest.mark.parametrize("case", REGISTRATION_DATA["positive_cases"], ids=lambda c: c["name"])
def test_registration_positive(page, case: dict) -> None:
    registration_page = RegistrationPage(page)
    registration_page.open_from_login()
    registration_page.register(
        first_name=case["first_name"],
        last_name=case["last_name"],
        address=case["address"],
        email=case["email"],
        phone_number=case["phone_number"],
        password=case["password"],
        confirm_password=case["confirm_password"],
    )

    assert page.url == Settings.MY_PRODUCTS_URL


@pytest.mark.parametrize("case", REGISTRATION_DATA["negative_cases"], ids=lambda c: c["name"])
def test_registration_negative(page, case: dict) -> None:
    registration_page = RegistrationPage(page)
    registration_page.open_from_login()
    registration_page.register(
        first_name=case["first_name"],
        last_name=case["last_name"],
        address=case["address"],
        email=case["email"],
        phone_number=case["phone_number"],
        password=case["password"],
        confirm_password=case["confirm_password"],
    )

    if "expected_messages" in case:
        for expected_message in case["expected_messages"]:
            assert registration_page.text_visible(expected_message)
    else:
        assert registration_page.text_visible(case["expected_message"])

