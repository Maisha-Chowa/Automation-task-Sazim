from playwright.sync_api import Page

from config import Settings


class BrowseProductsPage:
    BROWSE_PRODUCTS_NAV_TEXT = "Browse Products"

    TITLE_INPUT = "input[name='title']"
    CATEGORY_DROPDOWN = "div[name='category']"
    CATEGORY_OPTION = "div[role='option']"

    BUY_FILTER_CHECKBOX = "input[name='is_buy_filter_turned_on']"
    RENT_FILTER_CHECKBOX = "input[name='is_rent_filter_turned_on']"

    BUY_FILTER_LABEL_TEXT = "Buy Filters"
    RENT_FILTER_LABEL_TEXT = "Rent Filters"

    MIN_BUY_RANGE_INPUT = "input[name='min_buy_range']"
    MAX_BUY_RANGE_INPUT = "input[name='max_buy_range']"

    MIN_RENT_RANGE_INPUT = "input[name='min_rent_range']"
    MAX_RENT_RANGE_INPUT = "input[name='max_rent_range']"
    RENT_DURATION_DROPDOWN = "div[name='rent_duration_type']"

    CLEAR_BUTTON_TEXT = "Clear"
    FILTER_BUTTON_TEXT = "Filter"
    LOAD_MORE_BUTTON_TEXT = "Load More"

    PRODUCT_TITLE_TEXT = "div.sc-hKwDye"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def open_from_my_products(self) -> None:
        self.page.get_by_text(self.BROWSE_PRODUCTS_NAV_TEXT).first.click()
        self.page.wait_for_url(f"{Settings.BASE_URL}/browse-products")

    def is_on_browse_products_page(self) -> bool:
        return "/browse-products" in self.page.url

    def fill_title(self, title: str) -> None:
        self.page.locator(self.TITLE_INPUT).fill(title)

    def choose_category(self, category_name: str) -> None:
        self.page.locator(self.CATEGORY_DROPDOWN).click()
        self.page.locator(
            f"{self.CATEGORY_DROPDOWN} {self.CATEGORY_OPTION}",
            has_text=category_name,
        ).first.click()

    def enable_buy_filter(self) -> None:
        if not self.page.locator(self.BUY_FILTER_CHECKBOX).is_checked():
            self.page.get_by_text(self.BUY_FILTER_LABEL_TEXT, exact=True).first.click()

    def enable_rent_filter(self) -> None:
        if not self.page.locator(self.RENT_FILTER_CHECKBOX).is_checked():
            self.page.get_by_text(self.RENT_FILTER_LABEL_TEXT, exact=True).first.click()

    def set_buy_range(self, min_value: str, max_value: str) -> None:
        self.enable_buy_filter()
        self.page.locator(self.MIN_BUY_RANGE_INPUT).fill(min_value)
        self.page.locator(self.MAX_BUY_RANGE_INPUT).fill(max_value)

    def set_rent_range(self, min_value: str, max_value: str, duration_type: str) -> None:
        self.enable_rent_filter()
        self.page.locator(self.MIN_RENT_RANGE_INPUT).fill(min_value)
        self.page.locator(self.MAX_RENT_RANGE_INPUT).fill(max_value)
        self.page.locator(self.RENT_DURATION_DROPDOWN).click()
        self.page.locator(
            f"{self.RENT_DURATION_DROPDOWN} {self.CATEGORY_OPTION}",
            has_text=duration_type,
        ).first.click()

    def apply_filters(self) -> None:
        self.page.get_by_role("button", name=self.FILTER_BUTTON_TEXT).click()
        self.page.wait_for_timeout(800)

    def clear_filters(self) -> None:
        self.page.get_by_role("button", name=self.CLEAR_BUTTON_TEXT).click()
        self.page.wait_for_timeout(600)

    def product_titles(self) -> list[str]:
        return [title.strip() for title in self.page.locator(self.PRODUCT_TITLE_TEXT).all_text_contents() if title.strip()]

    def product_count(self) -> int:
        return len(self.product_titles())

    def text_visible(self, text: str) -> bool:
        return text in self.page.locator("body").inner_text()

