import os
import time
import pytest
import allure
from selene import browser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FxOptions


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    # Жёстко используем Firefox, без хромовых аргументов
    selenoid_url = os.getenv("SELENOID_URL", "https://user1:1234@selenoid.autotests.cloud/wd/hub").strip()
    browser_version = (os.getenv("BROWSER_VERSION") or "").strip()  # можно оставить пустым
    headless = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")

    opts = FxOptions()
    if headless:
        opts.add_argument("-headless")

    # Минимально необходимые capabilities для Selenoid
    opts.set_capability("browserName", "firefox")
    if browser_version:
        opts.set_capability("browserVersion", browser_version)
    opts.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True,
        "enableLog": True
    })

    driver = webdriver.Remote(command_executor=selenoid_url, options=opts)

    # Настраиваем Selene
    browser.config.driver = driver
    browser.config.timeout = float(os.getenv("SELENE_TIMEOUT", "6"))
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield

    try:
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception:
        pass

    try:
        session_id = browser.driver.session_id
        video_host = os.getenv("SELENOID_VIDEO_BASE", "https://selenoid.autotests.cloud/video").rstrip("/")
        video_url = f"{video_host}/{session_id}.mp4"

        time.sleep(2)
        html = (
            '<html><body style="margin:0">'
            f'<video width="100%" height="100%" controls>'
            f'<source src="{video_url}" type="video/mp4">'
            "Видео недоступно."
            "</video></body></html>"
        )
        allure.attach(html, name="Selenoid video", attachment_type=allure.attachment_type.HTML)
    except Exception as e:
        allure.attach(str(e), name="video_error", attachment_type=allure.attachment_type.TEXT)

    browser.quit()
