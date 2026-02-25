from playwright.sync_api import Page

from config import Settings


class LoginPage:
    EMAIL_INPUT = "input[name='email']"
    PASSWORD_INPUT = "input[name='password']"
    SIGN_IN_BUTTON = "button:has-text('Sign In')"
    SIGN_UP_LINK = "a[href='/register']"
    REQUIRED_PASSWORD_TEXT = "Password is required"
    INVALID_CREDENTIALS_TEXT = "Incorrect username or password. Please try again!"
    INVALID_EMAIL_FORMAT_TEXT = "Please enter a valid email address"
    MY_PRODUCTS_TEXT = "My Products"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def open(self) -> None:
        self.page.goto(Settings.LOGIN_URL, wait_until="domcontentloaded")

    def login(self, email: str, password: str) -> None:
        self.page.locator(self.EMAIL_INPUT).fill(email)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.SIGN_IN_BUTTON).click()

    def sign_up_link_visible(self) -> bool:
        return self.page.locator(self.SIGN_UP_LINK).is_visible()

    def is_on_login_page(self) -> bool:
        return "teebay-buggy" in self.page.url

    def invalid_credentials_message_visible(self) -> bool:
        try:
            self.page.get_by_text(self.INVALID_CREDENTIALS_TEXT).first.wait_for(state="visible")
            return True
        except Exception:
            return False

    def password_required_message_count(self) -> int:
        return self.page.get_by_text(self.REQUIRED_PASSWORD_TEXT).count()

    def text_visible(self, text: str) -> bool:
        try:
            self.page.get_by_text(text).first.wait_for(state="visible")
            return True
        except Exception:
            return False

    def my_products_visible(self) -> bool:
        try:
            self.page.get_by_text(self.MY_PRODUCTS_TEXT).first.wait_for(state="visible")
            return True
        except Exception:
            return False

