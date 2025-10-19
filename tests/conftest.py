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
    # Builds a proper Remote WebDriver URL from SELENOID_URL env.
    # Accepts forms with/without protocol and /wd/hub suffix.
    raw = (os.getenv("SELENOID_URL") or "https://user1:1234@selenoid.autotests.cloud/wd/hub").strip()
    if not raw.startswith("http"):
        raw = f"https://{raw}"
    if "/wd/hub" not in raw:
        if raw.endswith("/"):
            raw = raw[:-1]
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
        # Default to chrome, but WITHOUT any user-data-dir if value is empty
        opts = ChOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
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

    remote = _make_remote_url()
    print("[SELENOID] remote url:", remote)
    print("[SELENOID] caps:", json.dumps({
        "browserName": "firefox" if browser_name == "firefox" else "chrome",
        "browserVersion": version or "(auto)"
    }))

    return webdriver.Remote(command_executor=remote, options=opts)


def _wait_video_available(video_url: str, timeout_sec: int = 30, poll: float = 1.0) -> bool:
    # Polls Selenoid /video/<session>.mp4 until exists & has content
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            req = Request(video_url, headers={"User-Agent": "allure-video-check"})
            with urlopen(req, timeout=5) as r:
                if r.status == 200 and int(r.headers.get("Content-Length", "0")) > 1024:
                    return True
        except (URLError, HTTPError, TimeoutError, Exception):
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
        allure.attach(
            browser.driver.get_screenshot_as_png(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception:
        pass
    try:
        allure.attach(
            browser.driver.page_source,
            name="page_source",
            attachment_type=allure.attachment_type.HTML
        )
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
    available = _wait_video_available(video_url, timeout_sec=30, poll=1.0)

    try:
        html = (
            '<html><body style="margin:0;background:#000">'
            f'<video width="100%" height="100%" controls {"autoplay" if available else ""}>'
            f'<source src="{video_url}" type="video/mp4">Видео пока не доступно: {video_url}'
            "</video></body></html>"
        )
        allure.attach(html, name="Selenoid video", attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass

    if available:
        try:
            req = Request(video_url, headers={"User-Agent": "allure-video-download"})
            with urlopen(req, timeout=20) as r:
                data = r.read()
            os.makedirs("allure-results", exist_ok=True)
            mp4_path = os.path.join("allure-results", f"{session_id}.mp4")
            with open(mp4_path, "wb") as f:
                f.write(data)
            allure.attach.file(mp4_path, name="Selenoid video (mp4)", attachment_type=allure.attachment_type.MP4)
        except Exception as e:
            allure.attach(str(e), name="video_download_error", attachment_type=allure.attachment_type.TEXT)
