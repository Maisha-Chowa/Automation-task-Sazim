from playwright.sync_api import Page

from config import Settings


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def wait_for_text_visible(self, text: str) -> bool:
        try:
            self.page.get_by_text(text).first.wait_for(state="visible")
            return True
        except Exception:
            return False

    def body_text(self) -> str:
        return self.page.locator("body").inner_text()

    def body_contains(self, text: str) -> bool:
        return text in self.body_text()
