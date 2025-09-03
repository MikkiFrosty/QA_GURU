import os
import pytest
from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(autouse=True, scope='function')
def setup_browser():
    host = os.getenv('SELENOID_URL')            # selenoid.autotests.cloud
    login = os.getenv('SELENOID_LOGIN')
    password = os.getenv('SELENOID_PASS')

    options = Options()
    options.set_capability('browserName', 'chrome')
    options.set_capability('browserVersion', '128.0')
    options.set_capability('selenoid:options', {'enableVNC': True, 'name': 'ozon_deposit'})

    driver = webdriver.Remote(
        command_executor=f'https://{login}:{password}@{host}/wd/hub',
        options=options
    )

    browser.config.driver = driver
    browser.config.base_url = 'https://finance.ozon.ru'
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 6
    yield
    browser.quit()