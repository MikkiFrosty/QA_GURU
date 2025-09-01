import os
import calendar
from datetime import date
import allure
from selene import have, be, by
from selene import browser

from tests.models.deposit import Deposit_class
from tests.models.deposit_calculator_locators import DepositCalculatorLocators as L


class Deposit:
    def open_form(self):
        with allure.step("Переход на страницу"):
            browser.open('https://finance.ozon.ru/promo/deposit/landing')
            browser.driver.set_window_size(1920, 1080)
        return self

    def filling_field(self, deposit: Deposit_class):
        with allure.step("Вводим сумму"):
            if deposit.deposit_amount is not None:
                browser.element(L.AMOUNT).type(deposit.deposit_amount)
        with allure.step("Выбираем срок вклада"):
            if deposit.term is not None:
                browser.element(L.TERM_BTN(deposit.term)).click()
        return self

    def should_show_calc(self, deposit: Deposit_class):
        with allure.step('Проверяем результат калькулятора'):
            # сумма в инпуте
            if deposit.deposit_amount is not None:
                browser.element(L.AMOUNT).should(have.value(str(deposit.deposit_amount)))

            # «Вклад на N месяцев»
            if deposit.term is not None:
                browser.element(L.DEPOSIT_TYPE).should(have.text(str(deposit.term)))

            # ставка
            if deposit.interest_rate is not None:
                browser.element(L.RATE).should(have.text(str(deposit.interest_rate)))

            # доход
            if deposit.profit_amount is not None:
                browser.element(L.PROFIT).should(have.text(str(deposit.profit_amount)))

            # «к <дата>» — считаем от today + term, только если задан term
            if deposit.term is not None:
                today = date.today()
                y = today.year + (today.month - 1 + int(deposit.term)) // 12
                m = (today.month - 1 + int(deposit.term)) % 12 + 1
                d = min(today.day, calendar.monthrange(y, m)[1])
                browser.element(L.MATURITY).should(have.text(str(y))).should(have.text(str(d)))

            # инфо-блоки — проверяем только если в модели явно указаны флаги
            if getattr(deposit, 'check_capitalization', None):
                browser.element(L.CAPITALIZATION).should(be.visible)
            if getattr(deposit, 'check_insurance', None):
                browser.element(L.INSURANCE).should(be.visible)

        return self

    def should_have_active_buttons(self, deposit: Deposit_class = None):
        with allure.step('Проверяем кнопки'):
            # если в модели есть флаги, уважаем их; иначе проверяем обе
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