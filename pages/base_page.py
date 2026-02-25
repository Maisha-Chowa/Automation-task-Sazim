from playwright.sync_api import Page

from config import Settings


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def open(self, path: str = "") -> None:
        if path and not path.startswith("/"):
            path = f"/{path}"
        self.page.goto(f"{Settings.BASE_URL.rstrip('/')}{path}")

