import re
import time
from selenium.webdriver.common.keys import Keys
import allure
from selene import have, be, by, query
from selene import browser
from tests.models.deposit import DepositClass
from tests.models.deposit_calculator_locators import DepositCalculatorLocators as L


class Deposit:
    def open_form(self):
        with allure.step("Переход на страницу"):
            browser.open('https://finance.ozon.ru/promo/deposit/landing')
            browser.driver.set_window_size(1920, 1080)
        return self

    def filling_field(self, deposit: DepositClass):
        with allure.step("Вводим сумму"):
            if deposit.deposit_amount is not None:
                e = browser.element(L.AMOUNT)
                e.click()
                e.send_keys(Keys.CONTROL, 'a', Keys.DELETE)  # или Keys.BACKSPACE
                e.type(str(deposit.deposit_amount))

        with allure.step("Выбираем срок вклада"):
            if deposit.term is not None:
                browser.element(L.TERM_BTN(deposit.term)).click()
        return self

    def should_show_calc(self, deposit: DepositClass):
        with allure.step('Проверяем результат калькулятора'):

            time.sleep(1)

            if deposit.deposit_amount is not None:
                actual = browser.element(L.AMOUNT).get(query.value).replace(' ', '')
                expected = re.sub(r'\D', '', str(deposit.deposit_amount))
                assert actual == expected

            if getattr(deposit, 'deposit_type', None):
                browser.element(L.DEPOSIT_TYPE).should(have.text(str(deposit.deposit_type)))
            elif deposit.term is not None:
                browser.element(L.DEPOSIT_TYPE).should(have.text(str(deposit.term)))

            if deposit.interest_rate is not None:
                browser.element(L.RATE).should(have.text(str(deposit.interest_rate)))

            if deposit.profit_amount is not None:
                profit_text = browser.element(L.PROFIT).get(query.text).split("\n")[0].strip()
                expected_profit = str(deposit.profit_amount).strip()

                act_num = re.sub(r'[^\d,.-]', '', profit_text)
                exp_num = re.sub(r'[^\d,.-]', '', expected_profit)

                assert act_num == exp_num

            if getattr(deposit, 'check_capitalization', None):
                browser.element(L.CAPITALIZATION).should(be.visible)

        return self

    def should_have_active_buttons(self, deposit: DepositClass = None):
        with allure.step('Проверяем кнопки'):
            check_conditions = True
            check_cta = True
            if deposit is not None:
                check_conditions = getattr(deposit, 'check_conditions', True)
                check_cta = getattr(deposit, 'check_cta', True)

                if check_conditions:
                    browser.element(L.CONDITIONS).should(be.visible).should(be.enabled)
                if check_cta:
                    browser.element(L.CTA).should(be.visible).should(be.enabled)
                return self

    def should_have_stub(self):
        browser.element(L.STUB).should(be.visible)