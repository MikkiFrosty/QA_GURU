import pytest
from selene import browser, be, have
from tests.pages.deposit_page import Deposit as DepositPage
from tests.models.deposit import Deposit_class
from tests.models.deposit_calculator_locators import DepositCalculatorLocators as L


def test_deposit_valid():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount=150000,
        term=4,
        interest_rate="15,1%",
        profit_amount="+7 511,43 ₽",
        deposit_type="Вклад на 4 месяца",
        check_capitalization=True,
        check_insurance=True,
        check_conditions=True,
        check_cta=True,
    )
    page.filling_field(value) \
        .should_show_calc(value) \
        .should_have_active_buttons(value)


def test_deposit_min():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount=10000,
        term=4,
        interest_rate="15,1%",
        profit_amount="+500,76 ₽",
        check_capitalization=True,
        check_insurance=True,
    )
    page.filling_field(value).should_show_calc(value).should_have_active_buttons(value)


def test_deposit_invalid_sum_below_min():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount=9999,
        term=4
    )
    page.filling_field(value)
    browser.element(L.CTA).should(be.disabled)      # кнопка недоступна
    # при необходимости можно добавить: поле подсветилось/ошибка и т.п.


def test_deposit_invalid_symbols():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount="абвГДЕabcXYZ!@#$%^&*()",
        term=4
    )
    page.filling_field(value)
    browser.element(L.CTA).should(be.disabled)      # ввод невалиден → CTA неактивна

def test_form_display_smoke():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount=150000,
        term=3
    )
    page.filling_field(value).should_have_active_buttons()
    browser.element(L.RATE).should(be.visible)
    browser.element(L.PROFIT).should(be.visible)