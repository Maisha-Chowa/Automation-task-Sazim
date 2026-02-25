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


class Settings:
    BASE_URL = os.getenv(
        "BASE_URL",
        "https://ehsanur-rahman-sazim.github.io/teebay-buggy/",
    )
    BROWSER_NAME = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    DEFAULT_TIMEOUT_MS = _get_int_env("DEFAULT_TIMEOUT_MS", 15000)
