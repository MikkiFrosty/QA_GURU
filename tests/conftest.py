import os
import time
import json
import pytest
import allure

from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FxOptions
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def _make_remote_url() -> str:
    raw = (os.getenv("SELENOID_URL") or "https://user1:1234@selenoid.autotests.cloud/wd/hub").strip()
    if not raw.startswith("http"):
        raw = f"https://{raw}"
    if "/wd/hub" not in raw:
        raw = raw.rstrip("/")
        raw = f"{raw}/wd/hub"
    return raw


def _make_driver():
    browser_name = (os.getenv("BROWSER") or "firefox").lower().strip()
    version = (os.getenv("BROWSER_VERSION") or "").strip()
    headless = (os.getenv("HEADLESS") or "true").lower() in ("1", "true", "yes")

    if browser_name == "firefox":
        opts = FxOptions()
        if headless:
            opts.add_argument("-headless")
        opts.set_capability("browserName", "firefox")
        if version:
            opts.set_capability("browserVersion", version)
    else:
        opts = ChOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        # никаких user-data-dir без значения
        udd = (os.getenv("CHROME_USER_DATA_DIR") or "").strip()
        if udd:
            opts.add_argument(f"--user-data-dir={udd}")
        prof = (os.getenv("CHROME_PROFILE_DIR") or "").strip()
        if prof:
            opts.add_argument(f"--profile-directory={prof}")
        opts.set_capability("browserName", "chrome")
        if version:
            opts.set_capability("browserVersion", version)

    opts.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True,
        "enableLog": True,
        "name": os.getenv("BUILD_TAG", "ui-tests")
    })

    return webdriver.Remote(command_executor=_make_remote_url(), options=opts)


def _wait_video_ready(video_url: str, timeout_sec: int = 20, poll: float = 1.0) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            req = Request(video_url, headers={"User-Agent": "allure-video-check"})
            with urlopen(req, timeout=5) as r:
                if r.status == 200 and int(r.headers.get("Content-Length", "0")) > 1024:
                    return True
        except Exception:
            pass
        time.sleep(poll)
    return False


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    driver = _make_driver()
    browser.config.driver = driver
    browser.config.timeout = float(os.getenv("SELENE_TIMEOUT", "6"))
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield

    try:
        session_id = browser.driver.session_id
    except Exception:
        session_id = None

    try:
        allure.attach(browser.driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass
    try:
        allure.attach(browser.driver.page_source, name="page_source", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass

    try:
        browser.quit()
    except Exception:
        pass

    if not session_id:
        return

    video_base = (os.getenv("SELENOID_VIDEO_BASE") or "https://selenoid.autotests.cloud/video").rstrip("/")
    video_url = f"{video_base}/{session_id}.mp4"
    ready = _wait_video_ready(video_url, timeout_sec=20, poll=1.0)

    html = (
        '<html><body style="margin:0;background:#000">'
        f'<p style="color:#ccc;font:12px/1.4 monospace;margin:8px">'
        f'Источник: <a style="color:#9cf" href="{video_url}" target="_blank">{video_url}</a>'
        '</p>'
        f'<video width="100%" height="100%" controls {"autoplay" if ready else ""}>'
        f'<source src="{video_url}" type="video/mp4">Видео пока не доступно.'
        '</video></body></html>'
    )
    try:
        allure.attach(html, name="Selenoid video", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass
