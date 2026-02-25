from pages.base_page import BasePage


def test_home_page_opens(page) -> None:
    base_page = BasePage(page)
    base_page.open()

    assert "teebay-buggy" in page.url

