import os

from dotenv import load_dotenv


load_dotenv()


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip().strip('"').strip("'")
    try:
        return int(value)
    except ValueError:
        return default


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_str_env(name: str, default: str = "") -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().strip('"').strip("'")


class Settings:
    BASE_URL = _get_str_env(
        "BASE_URL"
    ).rstrip("/")
    LOGIN_URL = f"{BASE_URL}/teebay-buggy/"
    MY_PRODUCTS_URL = f"{BASE_URL}/my-products"
    BROWSER_NAME = _get_str_env("BROWSER", "chromium")
    HEADLESS = _get_bool_env("HEADLESS", True)
    DEFAULT_TIMEOUT_MS = _get_int_env("DEFAULT_TIMEOUT_MS", 15000)
    USERNAME = _get_str_env("USERNAME")
    PASSWORD = _get_str_env("PASSWORD")
