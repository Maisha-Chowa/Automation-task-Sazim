import pytest
from playwright.sync_api import Browser, BrowserContext, BrowserType, Page, Playwright, sync_playwright

from config import Settings


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    browser_type: BrowserType = getattr(playwright_instance, Settings.BROWSER_NAME)
    browser = browser_type.launch(headless=Settings.HEADLESS)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page

