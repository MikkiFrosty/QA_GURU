import os
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import allure


@pytest.fixture(scope="function")
def browser():
    browser_name = os.getenv("BROWSER", "firefox")
    selenoid_url = os.getenv("SELENOID_URL", "https://user1:1234@selenoid.autotests.cloud/wd/hub")

    if browser_name.lower() == "firefox":
        options = FirefoxOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Настройки для Selenoid
    options.set_capability("browserName", browser_name)
    options.set_capability("browserVersion", "125.0")
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True,
        "enableLog": True
    })

    driver = webdriver.Remote(
        command_executor=selenoid_url,
        options=options
    )

    driver.maximize_window()
    yield driver

    # Снятие видео и скриншотов после теста
    allure.attach(
        driver.get_screenshot_as_png(),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG
    )

    driver.quit()
