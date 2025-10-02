import os
import pytest
import allure
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def _build_local_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    if os.getenv("HEADLESS", "true").lower() in {"true", "1", "yes"}:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def _build_selenoid_driver():
    selenoid_url = os.getenv("SELENOID_URL")
    assert selenoid_url, "ENV SELENOID_URL is required (e.g. https://user:pass@selenoid.autotests.cloud/wd/hub)"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    caps = {
        "browserName": "chrome",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "name": os.getenv("BUILD_TAG", "ozon-deposit-ui"),
        },
    }
    return webdriver.Remote(
        command_executor=selenoid_url,
        options=options,
        desired_capabilities=caps,
    )


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    target = os.getenv("RUN_TARGET", "selenoid").lower()
    driver = _build_selenoid_driver() if target == "selenoid" else _build_local_driver()

    browser.config.driver = driver
    browser.config.base_url = "https://finance.ozon.ru"

    try:
        yield
    finally:
        # Allure attachments
        try:
            png = browser.driver.get_screenshot_as_png()
            allure.attach(png, name="last_screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

        try:
            session_id = browser.driver.session_id
            video_host = os.getenv("SELENOID_VIDEO_BASE", "https://selenoid.autotests.cloud/video")
            video_url = f"{video_host}/{session_id}.mp4"
            html = (
                '<html><body>'
                f'<video width="100%" height="100%" controls autoplay>'
                f'<source src="{video_url}" type="video/mp4"></video>'
                '</body></html>'
            )
            allure.attach(html, name="video", attachment_type=allure.attachment_type.HTML)
        except Exception:
            pass

        browser.quit()
