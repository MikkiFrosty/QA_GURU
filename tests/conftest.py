import os
import pytest
import allure

from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Автозагрузка .env из корня проекта
load_dotenv()

def _build_selenoid_remote():
    """Always run in Selenoid. URL built from pieces."""
    login = os.getenv('SELENOID_LOGIN', '').strip()
    password = os.getenv('SELENOID_PASS', '').strip()
    raw = os.getenv('SELENOID_URL', 'selenoid.autotests.cloud').strip()

    if '@' in raw and 'wd/hub' in raw:
        command_executor = raw if raw.startswith('http') else f"https://{raw}"
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

    # capabilities через set_capability
    opts.set_capability('browserName', 'chrome')
    opts.set_capability('selenoid:options', {
        'enableVNC': True,
        'enableVideo': True,
    })
    opts.set_capability('name', os.getenv('BUILD_TAG', 'ui-tests'))
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Remote(
        command_executor=command_executor,
        options=opts
    )
    return driver


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    driver = _build_selenoid_remote()
    browser.config.driver = driver
    browser.config.base_url = os.getenv('BASE_URL', 'https://finance.ozon.ru')
    browser.config.timeout = float(os.getenv('SELENE_TIMEOUT', 6))

    yield

    # Allure attachments
    try:
        png = browser.driver.get_screenshot_as_png()
        allure.attach(png, name="last_screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass

    try:
        html = browser.driver.page_source
        allure.attach(html, name="page_source", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass

    try:
        logs = browser.driver.get_log("browser")
        allure.attach(str(logs), name="browser_console_logs", attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass

    try:
        session_id = browser.driver.session_id
        video_host = os.getenv("SELENOID_VIDEO_BASE", "https://selenoid.autotests.cloud/video")
        video_url = f"{video_host}/{session_id}.mp4"
        html = f'<html><body><video width="100%" height="100%" controls autoplay><source src="{video_url}" type="video/mp4"></video></body></html>'
        allure.attach(html, name="video", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass

    browser.quit()
