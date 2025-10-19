import os
import time
import pytest
import requests
import allure
from selene import browser
from selenium import webdriver


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "120.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "enableLog": True
        }
    }

    options = webdriver.ChromeOptions()
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=os.getenv("SELENOID_URL", "https://user1:1234@selenoid.autotests.cloud/wd/hub"),
        options=options
    )
    browser.config.driver = driver
    browser.config.timeout = 6
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    # Allure attachments
    try:
        allure.attach(browser.driver.get_screenshot_as_png(), name="last_screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass

    try:
        allure.attach(browser.driver.page_source, name="page_source", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass

    try:
        logs = browser.driver.get_log("browser")
        log_text = "\n".join([f"{l['level']}: {l['message']}" for l in logs])
        allure.attach(log_text, name="browser_console_logs", attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass

    try:
        session_id = browser.driver.session_id
        video_host = os.getenv("SELENOID_VIDEO_BASE", "https://selenoid.autotests.cloud/video").rstrip("/")
        video_url = f"{video_host}/{session_id}.mp4"
        time.sleep(3)
        resp = requests.get(video_url, timeout=15)
        if resp.ok and len(resp.content) > 1024:
            os.makedirs("allure-results", exist_ok=True)
            path = f"allure-results/{session_id}.mp4"
            with open(path, "wb") as f:
                f.write(resp.content)
            allure.attach.file(path, name="Selenoid video", attachment_type=allure.attachment_type.MP4)
        else:
            html = f'<html><body><video width="100%" height="100%" controls autoplay><source src="{video_url}" type="video/mp4"></video></body></html>'
            allure.attach(html, name="Selenoid video (link)", attachment_type=allure.attachment_type.HTML)
    except Exception as e:
        allure.attach(str(e), name="video_error", attachment_type=allure.attachment_type.TEXT)

    browser.quit()
