import pytest
from selene import browser

@pytest.fixture(autouse=True)
def setup_browser(remote_browser_setup):
    browser.config.base_url = 'https://finance.ozon.ru/promo/deposit/landing'
    browser.config.timeout = 5
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield