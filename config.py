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
        "BASE_URL")
    BROWSER_NAME = os.getenv("BROWSER")
    HEADLESS = os.getenv("HEADLESS")
    DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS"))
