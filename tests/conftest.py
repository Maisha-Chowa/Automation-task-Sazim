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


@pytest.fixture()
def authenticated_context(browser: Browser) -> BrowserContext:
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture()
def authenticated_page(authenticated_context: BrowserContext) -> Page:
    page = authenticated_context.new_page()

    if not Settings.USERNAME or not Settings.PASSWORD:
        raise RuntimeError("USERNAME/PASSWORD are required for authenticated_page.")

    page.goto(Settings.LOGIN_URL, wait_until="domcontentloaded")
    page.locator("input[name='email']").fill(Settings.USERNAME)
    page.locator("input[name='password']").fill(Settings.PASSWORD)
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_timeout(1500)

    if page.url != Settings.MY_PRODUCTS_URL:
        raise RuntimeError(f"Authenticated page setup failed. Current URL: {page.url}")

    yield page
    page.close()

