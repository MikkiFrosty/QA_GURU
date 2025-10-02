import os
import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import allure
from utils import attach


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    base_url = os.getenv("BASE_URL", "https://finance.ozon.ru")
    remote = os.getenv("REMOTE", "false").lower() == "true"

    options = ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if remote:
        # читаем креды и URL
        login = os.getenv("SELENOID_LOGIN")
        password = os.getenv("SELENOID_PASS")
        selenoid_url = os.getenv("SELENOID_URL", "selenoid.autotests.cloud/wd/hub").replace("http://", "").replace("https://", "")

        capabilities = {
            "browserName": "chrome",
            "browserVersion": "100.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }

        executor = f"https://{selenoid_url}"

        # передаём креды через remote_connection (новый формат Selenium не глотает login:pass в URL)
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        conn = RemoteConnection(executor, resolve_ip=False)
        conn.set_auth((login, password))

        driver = webdriver.Remote(
            command_executor=conn,
            options=options,
            desired_capabilities=capabilities
        )

    else:
        driver = webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.config.base_url = base_url
    browser.config.timeout = float(os.getenv("SELENE_TIMEOUT", "6"))
    browser.driver.set_window_size(
        int(os.getenv("WINDOW_WIDTH", "1920")),
        int(os.getenv("WINDOW_HEIGHT", "1080"))
    )

    yield

    # добавляем вложения в Allure
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
