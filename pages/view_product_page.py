import re
from datetime import date, timedelta

from playwright.sync_api import Page

from config import Settings


class ViewProductPage:
    BROWSE_PRODUCTS_NAV_TEXT = "Browse Products"
    CLEAR_BUTTON_TEXT = "Clear"
    FILTER_BUTTON_TEXT = "Filter"
    CATEGORY_DROPDOWN = "div[name='category']"
    CATEGORY_OPTION = "div[role='option']"

    BUY_BUTTON_TEXT = "Buy"
    RENT_BUTTON_TEXT = "Rent"
    BUY_CONFIRM_BUTTON_TEXT = "Yes!"
    BUY_CANCEL_BUTTON_TEXT = "Cancel"
    RENT_BOOK_BUTTON_TEXT = "Book rent"
    RENT_CANCEL_BUTTON_TEXT = "Cancel"

    MODAL_SELECTOR = "div.ui.modal.transition.visible.active"

    START_DATE_INPUT = "input[name='start_date']"
    END_DATE_INPUT = "input[name='end_date']"

    PRODUCT_TITLE_TEXT = "div.sc-hKwDye"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def open_browse_products(self) -> None:
        self.page.get_by_text(self.BROWSE_PRODUCTS_NAV_TEXT).first.click()
        self.page.wait_for_url(f"{Settings.BASE_URL}/browse-products")
        clear_button = self.page.get_by_role("button", name=self.CLEAR_BUTTON_TEXT)
        if clear_button.count() > 0:
            clear_button.first.click()
            self.page.wait_for_timeout(300)

    def choose_category_and_filter(self, category_name: str) -> None:
        self.page.locator(self.CATEGORY_DROPDOWN).click()
        self.page.locator(
            f"{self.CATEGORY_DROPDOWN} {self.CATEGORY_OPTION}",
            has_text=category_name,
        ).first.click()
        self.page.get_by_role("button", name=self.FILTER_BUTTON_TEXT).click()
        self.page.wait_for_timeout(500)

    def open_product_by_title(self, product_title: str, category: str | None = None) -> None:
        self.open_browse_products()
        if category:
            self.choose_category_and_filter(category)
        product_title_locator = self.page.locator(self.PRODUCT_TITLE_TEXT, has_text=product_title)
        if product_title_locator.count() == 0:
            raise ValueError(f"Product not found in browse list: {product_title}")
        product_title_locator.first.click()
        self.page.wait_for_timeout(500)

    def open_first_available_non_owned_product(self) -> str:
        self.open_browse_products()
        titles = [title.strip() for title in self.page.locator(self.PRODUCT_TITLE_TEXT).all_text_contents() if title.strip()]

        for title in titles:
            self.open_product_by_title(title)
            if (
                self.status_text().lower() == "available"
                and not self.is_owned_by_logged_user()
                and self.buy_button_visible()
                and self.rent_button_visible()
            ):
                return title

        raise RuntimeError("No available non-owned product found with Buy/Rent actions.")

    def status_text(self) -> str:
        body = self.page.locator("body").inner_text()
        match = re.search(r"Status:\s*([A-Za-z]+)", body, flags=re.IGNORECASE)
        if not match:
            return ""
        return match.group(1).strip()

    def is_owned_by_logged_user(self) -> bool:
        body = self.page.locator("body").inner_text().lower()
        return "you own this product" in body or "you own the product" in body

    def buy_button_visible(self) -> bool:
        return self.page.get_by_role("button", name=self.BUY_BUTTON_TEXT).count() > 0

    def rent_button_visible(self) -> bool:
        return self.page.get_by_role("button", name=self.RENT_BUTTON_TEXT).count() > 0

    def open_buy_modal(self) -> None:
        self.page.get_by_role("button", name=self.BUY_BUTTON_TEXT).click()
        self.page.locator(self.MODAL_SELECTOR).wait_for(state="visible")

    def confirm_buy(self) -> None:
        self.page.get_by_role("button", name=self.BUY_CONFIRM_BUTTON_TEXT).click()
        self.page.wait_for_timeout(900)

    def cancel_buy(self) -> None:
        self.page.get_by_role("button", name=self.BUY_CANCEL_BUTTON_TEXT).click()
        self.page.wait_for_timeout(400)

    def open_rent_modal(self) -> None:
        self.page.get_by_role("button", name=self.RENT_BUTTON_TEXT).click()
        self.page.locator(self.MODAL_SELECTOR).wait_for(state="visible")

    def set_rent_dates(self, start_date: str, end_date: str) -> None:
        self.page.locator(self.START_DATE_INPUT).fill(start_date)
        self.page.locator(self.END_DATE_INPUT).fill(end_date)

    def set_rent_dates_from_offsets(self, start_offset_days: int, end_offset_days: int) -> None:
        today = date.today()
        start_date = str(today + timedelta(days=start_offset_days))
        end_date = str(today + timedelta(days=end_offset_days))
        self.set_rent_dates(start_date, end_date)

    def book_rent(self) -> None:
        self.page.get_by_role("button", name=self.RENT_BOOK_BUTTON_TEXT).click()
        self.page.wait_for_timeout(1000)

    def cancel_rent(self) -> None:
        self.page.get_by_role("button", name=self.RENT_CANCEL_BUTTON_TEXT).click()
        self.page.wait_for_timeout(400)

    def rent_book_button_disabled(self) -> bool:
        return self.page.get_by_role("button", name=self.RENT_BOOK_BUTTON_TEXT).is_disabled()

