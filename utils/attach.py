import os
import allure
from allure_commons.types import AttachmentType
from selene.support.shared import browser


def add_screenshot(_browser=browser):
    try:
        allure.attach(
            _browser.driver.get_screenshot_as_png(),
            name='screenshot',
            attachment_type=AttachmentType.PNG,
        )
    except Exception:
        pass


def add_html(_browser=browser):
    try:
        allure.attach(
            _browser.driver.page_source,
            name='page_source',
            attachment_type=AttachmentType.HTML,
        )
    except Exception:
        pass


def add_logs(_browser=browser):
    try:
        logs = '\n'.join(
            f'[{line["level"]}] {line["message"]}'
            for line in _browser.driver.get_log('browser')
        )
        allure.attach(logs, name='browser_console', attachment_type=AttachmentType.TEXT)
    except Exception:
        pass


def add_video(_browser=browser):
    try:
        session = _browser.driver.session_id
        host = os.getenv('SELENOID_URL', 'selenoid.autotests.cloud') \
                  .replace('http://', '').replace('https://', '').rstrip('/')
        url = f'https://{host}/video/{session}.mp4'
        allure.attach(url, name='video_url', attachment_type=AttachmentType.URI_LIST)
    except Exception:
        pass