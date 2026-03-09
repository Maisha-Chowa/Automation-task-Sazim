import os
from dotenv import load_dotenv
load_dotenv()


class Settings:
    BASE_URL = os.getenv("BASE_URL", "").rstrip("/")
    LOGIN_URL = f"{BASE_URL}/teebay-buggy/"
    MY_PRODUCTS_URL = f"{BASE_URL}/my-products"
    ACCOUNT_SETTINGS_URL = f"{BASE_URL}/account-settings"
    BROWSER_NAME = os.getenv("BROWSER", "chromium")
    HEADLESS = os.getenv("HEADLESS", "true").strip().lower() in {"1", "true", "yes", "on"}
    DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "15000"))
    USERNAME = os.getenv("USERNAME", "")
    PASSWORD = os.getenv("PASSWORD", "")
