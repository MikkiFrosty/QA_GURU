import os
import pytest
import allure

from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Autoload .env from workspace root
load_dotenv()

def _build_selenoid_remote():
    """Always run in Selenoid. URL built from pieces."""
    login = os.getenv('SELENOID_LOGIN', '').strip()
    password = os.getenv('SELENOID_PASS', '').strip()
    raw = os.getenv('SELENOID_URL', 'selenoid.autotests.cloud').strip()

    # If full url with creds is provided
    if ('@' in raw) and ('wd/hub' in raw):
        command_executor = raw if raw.startswith('http') else f'https://{raw}'
    else:
        host = raw.replace('http://', '').replace('https://', '').rstrip('/')
        if 'wd/hub' not in host:
            host = f'{host}/wd/hub'
        if not login or not password:
            raise RuntimeError('ENV SELENOID_LOGIN/SELENOID_PASS are required to build Selenoid URL')
        command_executor = f'https://{login}:{password}@{host}'

    opts = Options()
    opts.add_argument('--window-size=1920,1080')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    if os.getenv('HEADLESS', 'true').lower() in ('1', 'true', 'yes'):
        opts.add_argument('--headless=new')

    caps = {
        'browserName': 'chrome',
        'selenoid:options': {
            'enableVNC': True,
            'enableVideo': True,
        },
        'name': os.getenv('BUILD_TAG', 'ui-tests'),
    }

    driver = webdriver.Remote(
        command_executor=command_executor,
        options=opts,
        desired_capabilities=caps,
    )
    return driver


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    driver = _build_selenoid_remote()

    browser.config.driver = driver
    browser.config.base_url = os.getenv('BASE_URL', 'https://finance.ozon.ru')
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = float(os.getenv('SELENE_TIMEOUT', '6'))

    try:
        yield browser
    finally:
        with allure.step('Attachments & Teardown'):
            try:
                from utils.attach import add_screenshot, add_html, add_logs, add_video
                add_screenshot(browser)
                add_html(browser)
                add_logs(browser)
                add_video(browser)
            except Exception:
                pass
        browser.quit()
