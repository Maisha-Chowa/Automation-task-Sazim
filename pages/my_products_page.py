from playwright.sync_api import Page

from config import Settings


class MyProductsPage:
    PAGE_HEADING_TEXT = "My Products"
    MY_PRODUCTS_NAV_TEXT = "My Products"
    PRODUCT_TITLE_TEXT = "div.sc-hKwDye"
    PRODUCT_ROW = "div.sc-jrQzAO"
    DELETE_BUTTON = "button.ui.icon.button"
    ADD_PRODUCT_NAV_TEXT = "Add Product"
    DELETE_CONFIRM_MODAL = "div.ui.modal.transition.visible.active"
    DELETE_MODAL_TEXT = "Are you sure you want to delete this product?"
    DELETE_CONFIRM_BUTTON_TEXT = "Yes, delete"
    DELETE_CANCEL_BUTTON_TEXT = "Cancel"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def open(self) -> None:
        # Avoid direct deep-link loads on GitHub Pages; prefer in-app navbar navigation.
        if "my-products" in self.page.url:
            return
        if self.page.get_by_text(self.MY_PRODUCTS_NAV_TEXT).count() > 0:
            self.page.get_by_text(self.MY_PRODUCTS_NAV_TEXT).first.click()
            self.page.wait_for_timeout(800)

    def is_on_my_products_page(self) -> bool:
        return "my-products" in self.page.url

    def text_visible(self, text: str) -> bool:
        return text in self.page.locator("body").inner_text()

    def product_count(self, product_title: str) -> int:
        return self.page.locator(self.PRODUCT_TITLE_TEXT, has_text=product_title).count()

    def click_delete_for_product(self, product_title: str) -> None:
        row = self.page.locator(self.PRODUCT_ROW, has=self.page.locator(self.PRODUCT_TITLE_TEXT, has_text=product_title)).first
        row.locator(self.DELETE_BUTTON).click()

    def delete_modal_visible(self) -> bool:
        return self.page.locator(self.DELETE_CONFIRM_MODAL).count() > 0 and self.text_visible(self.DELETE_MODAL_TEXT)

    def confirm_delete(self) -> None:
        self.page.get_by_role("button", name=self.DELETE_CONFIRM_BUTTON_TEXT).click()

    def cancel_delete(self) -> None:
        self.page.get_by_role("button", name=self.DELETE_CANCEL_BUTTON_TEXT).click()

    def add_product_nav_visible(self) -> bool:
        return self.page.get_by_text(self.ADD_PRODUCT_NAV_TEXT).first.is_visible()


class AddUpdateProductPage:
    MY_PRODUCTS_NAV_TEXT = "My Products"
    ADD_PRODUCT_NAV_TEXT = "Add Product"
    PAGE_HEADING_TEXT = "ADD PRODUCT"
    EDIT_PAGE_HEADING_TEXT = "EDIT PRODUCT"

    TITLE_INPUT = "input[name='title']"
    DESCRIPTION_INPUT = "textarea[name='description']"
    PURCHASE_PRICE_INPUT = "input[name='purchase_price']"
    RENT_PRICE_INPUT = "input[name='rent_price']"
    CATEGORIES_DROPDOWN = "div[name='categories']"
    RENT_DURATION_DROPDOWN = "div[name='rent_duration_type']"
    CATEGORY_OPTION = "div[role='option']"
    SUBMIT_BUTTON = "button:has-text('Add Product')"

    NEED_OPTION_TEXT = "Need to select an option"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.set_default_timeout(Settings.DEFAULT_TIMEOUT_MS)

    def open_from_my_products(self) -> None:
        if "my-products" not in self.page.url and self.page.get_by_text(self.MY_PRODUCTS_NAV_TEXT).count() > 0:
            self.page.get_by_text(self.MY_PRODUCTS_NAV_TEXT).first.click()
            self.page.wait_for_timeout(800)
        self.page.get_by_text(self.ADD_PRODUCT_NAV_TEXT).first.click()
        self.page.wait_for_url(f"{Settings.BASE_URL}/add-product")

    def choose_category(self, category_name: str) -> None:
        self.page.locator(self.CATEGORIES_DROPDOWN).click()
        self.page.locator(f"{self.CATEGORIES_DROPDOWN} {self.CATEGORY_OPTION}", has_text=category_name).first.click()

    def choose_rent_duration(self, rent_duration_type: str) -> None:
        self.page.locator(self.RENT_DURATION_DROPDOWN).click()
        self.page.locator(
            f"{self.RENT_DURATION_DROPDOWN} {self.CATEGORY_OPTION}",
            has_text=rent_duration_type,
        ).first.click()

    def fill_form(
        self,
        title: str,
        description: str,
        purchase_price: str,
        rent_price: str,
    ) -> None:
        self.page.locator(self.TITLE_INPUT).fill(title)
        self.page.locator(self.DESCRIPTION_INPUT).fill(description)
        self.page.locator(self.PURCHASE_PRICE_INPUT).fill(purchase_price)
        self.page.locator(self.RENT_PRICE_INPUT).fill(rent_price)

    def submit(self) -> None:
        self.page.locator(self.SUBMIT_BUTTON).click()

    def submit_product(
        self,
        title: str,
        description: str,
        purchase_price: str,
        rent_price: str,
        category: str,
        rent_duration_type: str,
    ) -> None:
        self.fill_form(title, description, purchase_price, rent_price)
        self.choose_category(category)
        self.choose_rent_duration(rent_duration_type)
        self.submit()

    def is_on_add_product_page(self) -> bool:
        return self.page.url.endswith("/add-product")

    def is_on_edit_product_page(self) -> bool:
        return "/edit-product/" in self.page.url

    def go_to_my_products(self) -> None:
        self.page.get_by_text(self.MY_PRODUCTS_NAV_TEXT).first.click()
        self.page.wait_for_url(Settings.MY_PRODUCTS_URL)

    def open_existing_product_for_update(self, product_title_contains: str) -> None:
        if "my-products" not in self.page.url:
            self.page.goto(Settings.MY_PRODUCTS_URL, wait_until="domcontentloaded")
        self.page.get_by_text(product_title_contains).first.click()
        self.page.wait_for_url("**/edit-product/**")

    def text_visible(self, text: str) -> bool:
        return text in self.page.locator("body").inner_text()

    def product_visible_on_my_products(self, product_title: str) -> bool:
        return self.text_visible(product_title)

