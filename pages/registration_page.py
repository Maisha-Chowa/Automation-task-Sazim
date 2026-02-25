from playwright.sync_api import Page

from config import Settings


class RegistrationPage:
    FIRST_NAME_INPUT = "input[name='firstName']"
    LAST_NAME_INPUT = "input[name='lastName']"
    ADDRESS_INPUT = "input[name='address']"
    EMAIL_INPUT = "input[name='email']"
    PHONE_NUMBER_INPUT = "input[name='phoneNumber']"
    PASSWORD_INPUT = "input[name='password']"
    CONFIRM_PASSWORD_INPUT = "input[name='confirmPassword']"
    REGISTER_BUTTON = "button:has-text('Register')"
    SIGN_IN_LINK = "a[href='/signin']"

    INVALID_EMAIL_TEXT = "Please enter a valid email address"
    PASSWORD_REQUIRED_TEXT = "Password is required"
    EMAIL_REQUIRED_TEXT = "Email is required"
    PHONE_REQUIRED_TEXT = "Phone number is required"
    LAST_NAME_REQUIRED_TEXT = "Last Name is required"
    ADDRESS_REQUIRED_TEXT = "Address is required"
    INTERNAL_ERROR_TEXT = "Internal error occurred. Please check the server!"
    PAGE_HEADING_TEXT = "REGISTRATION"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def open_from_login(self) -> None:
        self.page.goto(Settings.LOGIN_URL, wait_until="domcontentloaded")
        self.page.get_by_role("link", name="Sign Up").click()
        self.page.wait_for_load_state("domcontentloaded")

    def register(
        self,
        first_name: str,
        last_name: str,
        address: str,
        email: str,
        phone_number: str,
        password: str,
        confirm_password: str,
    ) -> None:
        self.page.locator(self.FIRST_NAME_INPUT).fill(first_name)
        self.page.locator(self.LAST_NAME_INPUT).fill(last_name)
        self.page.locator(self.ADDRESS_INPUT).fill(address)
        self.page.locator(self.EMAIL_INPUT).fill(email)
        self.page.locator(self.PHONE_NUMBER_INPUT).fill(phone_number)
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        self.page.locator(self.CONFIRM_PASSWORD_INPUT).fill(confirm_password)
        self.page.locator(self.REGISTER_BUTTON).click()

    def is_on_registration_page(self) -> bool:
        return "/register" in self.page.url

    def text_visible(self, text: str) -> bool:
        try:
            self.page.get_by_text(text).first.wait_for(state="visible")
            return True
        except Exception:
            return False

    def any_text_visible(self, texts: list[str]) -> bool:
        return any(self.text_visible(text) for text in texts)

