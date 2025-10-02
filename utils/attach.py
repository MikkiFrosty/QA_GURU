import os
import allure

def _video_base():
    base = os.getenv('SELENOID_VIDEO_BASE') or os.getenv('VIDEO_HOST')
    if base:
        base = base.replace('http://', '').replace('https://', '').rstrip('/')
        return f'https://{base}/video'
    return 'https://selenoid.autotests.cloud/video'


def add_screenshot(browser):
    try:
        png = browser.driver.get_screenshot_as_png()
        allure.attach(png, name='last_screenshot', attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass


def add_html(browser):
    try:
        html = browser.driver.page_source
        allure.attach(html, name='page_source', attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass


def add_logs(browser):
    try:
        logs = '\n'.join([f"[{l['level']}] {l['message']}" for l in browser.driver.get_log('browser')])
        if logs.strip():
            allure.attach(logs, name='browser_console', attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass


def add_video(browser):
    try:
        session_id = browser.driver.session_id
        video_url = f"{_video_base()}/{session_id}.mp4"
        html = (
            "<html><body>"
            f"<video width='100%' height='100%' controls autoplay>"
            f"<source src='{video_url}' type='video/mp4'>"
            "</video>"
            "</body></html>"
        )
        allure.attach(html, name='video', attachment_type=allure.attachment_type.HTML)
    except Exception:
        pass
