from playwright.sync_api import Page

from config import Settings


class AccountSettingsPage:
    ACCOUNT_SETTINGS_NAV_TEXT = "Account Settings"
    PAGE_HEADING_TEXT = "ACCOUNT SETTINGS"

    FIRST_NAME_INPUT = "input[name='first_name']"
    LAST_NAME_INPUT = "input[name='last_name']"
    ADDRESS_INPUT = "input[name='address']"
    EMAIL_INPUT = "input[name='email']"
    PHONE_NUMBER_INPUT = "input[name='phone_number']"
    UPDATE_BUTTON = "button:has-text('Update')"

    UPDATE_SUCCESS_TEXT = "User updated!"
    MY_PRODUCTS_NAV_TEXT = "My Products"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def open_from_my_products(self) -> None:
        # Direct /my-products navigation is not stable on GitHub Pages; use current authenticated app page.
        if "account-settings" in self.page.url and self.page.locator(f"text={self.MY_PRODUCTS_NAV_TEXT}").count() > 0:
            self.go_to_my_products()
        elif "my-products" not in self.page.url:
            self.page.goto(Settings.LOGIN_URL, wait_until="domcontentloaded")
        self.page.locator(f"text={self.ACCOUNT_SETTINGS_NAV_TEXT}").first.click()
        self.page.wait_for_url(Settings.ACCOUNT_SETTINGS_URL)

    def update_account(
        self,
        first_name: str,
        last_name: str,
        address: str,
        email: str,
        phone_number: str,
    ) -> None:
        self.page.locator(self.FIRST_NAME_INPUT).fill(first_name)
        self.page.locator(self.LAST_NAME_INPUT).fill(last_name)
        self.page.locator(self.ADDRESS_INPUT).fill(address)
        self.page.locator(self.EMAIL_INPUT).fill(email)
        self.page.locator(self.PHONE_NUMBER_INPUT).fill(phone_number)
        self.page.locator(self.UPDATE_BUTTON).click()

    def is_on_account_settings_page(self) -> bool:
        return self.page.url == Settings.ACCOUNT_SETTINGS_URL

    def go_to_my_products(self) -> None:
        self.page.locator(f"text={self.MY_PRODUCTS_NAV_TEXT}").first.click()
        self.page.wait_for_url(Settings.MY_PRODUCTS_URL)

    def visible_text(self) -> str:
        return self.page.locator("body").inner_text()

    def text_visible(self, text: str) -> bool:
        return text in self.visible_text()

    def current_form_values(self) -> dict:
        return {
            "first_name": self.page.locator(self.FIRST_NAME_INPUT).input_value(),
            "last_name": self.page.locator(self.LAST_NAME_INPUT).input_value(),
            "address": self.page.locator(self.ADDRESS_INPUT).input_value(),
            "email": self.page.locator(self.EMAIL_INPUT).input_value(),
            "phone_number": self.page.locator(self.PHONE_NUMBER_INPUT).input_value(),
        }

