import os
import time
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def _remote_url() -> str:
    host = os.getenv("SELENOID_URL", "selenoid.autotests.cloud").strip()
    login = os.getenv("SELENOID_LOGIN", "").strip()
    password = os.getenv("SELENOID_PASS", "").strip()

    if login and password:
        return f"https://{login}:{password}@{host}/wd/hub"
    return f"https://{host}/wd/hub"


def _video_base() -> str:
    return os.getenv("SELENOID_VIDEO_BASE", "https://selenoid.autotests.cloud/video").rstrip("/")


@pytest.fixture(scope="session")
def browser_name():
    return os.getenv("BROWSER", "chrome").lower()


@pytest.fixture(scope="session")
def browser_version():
    return os.getenv("BROWSER_VERSION", "128.0")


@pytest.fixture
def browser(request, browser_name, browser_version):
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "videoFrameRate": 24,
            "screenResolution": "1920x1080x24",
        },
    }

    driver = webdriver.Remote(
        command_executor=_remote_url(),
        options=options,
        desired_capabilities=capabilities
    )

    time.sleep(1)

    yield driver

    session_id = driver.session_id
    driver.quit()

    time.sleep(1)

    video_url = f"{_video_base()}/{session_id}.mp4"
    html = (
        f"<html><body>"
        f"<video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'>"
        f"</video>"
        f"</body></html>"
    )
    allure.attach(html, name="Selenoid video", attachment_type=allure.attachment_type.HTML)