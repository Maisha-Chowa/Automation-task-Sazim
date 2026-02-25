import json
from pathlib import Path

import pytest

from config import Settings
from pages.login_page import LoginPage


def _load_login_data() -> dict:
    data_path = Path(__file__).resolve().parent.parent / "test_data" / "login.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


def _resolve_secret(value: str) -> str:
    if value == "{{USERNAME}}":
        return Settings.USERNAME
    if value == "{{PASSWORD}}":
        return Settings.PASSWORD
    return value


LOGIN_DATA = _load_login_data()


@pytest.mark.parametrize("case", LOGIN_DATA["ui_validations"], ids=lambda c: c["name"])
def test_login_ui_validation(page, case: dict) -> None:
    login_page = LoginPage(page)
    login_page.open()

    assert login_page.is_on_login_page()
    assert page.locator(login_page.EMAIL_INPUT).is_visible()
    assert page.locator(login_page.PASSWORD_INPUT).is_visible()
    assert page.locator(login_page.SIGN_IN_BUTTON).is_visible()
    assert login_page.sign_up_link_visible()


@pytest.mark.parametrize("case", LOGIN_DATA["positive_cases"], ids=lambda c: c["name"])
def test_login_positive(page, case: dict) -> None:
    email = _resolve_secret(case["email"])
    password = _resolve_secret(case["password"])
    if not email or not password:
        pytest.skip("Positive login credentials are not configured.")

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(email=email, password=password)

    assert page.url == Settings.MY_PRODUCTS_URL
    assert login_page.my_products_visible()


@pytest.mark.parametrize("case", LOGIN_DATA["negative_cases"], ids=lambda c: c["name"])
def test_login_negative(page, case: dict) -> None:
    email = _resolve_secret(case["email"])
    password = _resolve_secret(case["password"])

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(email=email, password=password)

    expected_message = case["expected_message"]
    assert login_page.text_visible(expected_message)

