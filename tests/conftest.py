import pytest
from selene.support.shared import browser
from selenium import webdriver

@pytest.fixture(autouse=True, scope='session')
def setup_browser():
    opts = webdriver.ChromeOptions()
    opts.set_capability('acceptInsecureCerts', True)
    driver = webdriver.Chrome(options=opts)
    browser.config.driver = driver

    browser.config.base_url = 'https://finance.ozon.ru'
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 5
    yield
    browser.quit()