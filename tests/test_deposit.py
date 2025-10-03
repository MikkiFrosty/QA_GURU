import allure
import pytest
from selene import browser, be, have
from tests.pages.deposit_page import Deposit as DepositPage
from tests.models.deposit import Deposit_class
from tests.models.deposit_calculator_locators import DepositCalculatorLocators as L

@allure.epic("Ozon Deposit")
@allure.feature("Позитивные сценарии")
@allure.story("Корректные данные")
@allure.tag('ui', 'deposit', 'positive')
def test_deposit_valid():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount=150000,
        term=4,
        interest_rate="14,8%",
        profit_amount="+7 361,87 ₽",
        deposit_type="Вклад на 4 месяца",
        check_capitalization=True,
        check_insurance=True,
        check_conditions=True,
        check_cta=True,
    )
    page.filling_field(value) \
        .should_show_calc(value) \
        .should_have_active_buttons(value)
@allure.epic("Ozon Deposit")
@allure.feature("Позитивные сценарии")
@allure.story("Ровно минимальная сумма")
@allure.tag('ui', 'deposit', 'boundary', 'positive')
def test_deposit_min():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount=10000,
        term=4,
        interest_rate="14,8%",
        profit_amount="+490,79 ₽",
        check_capitalization=True,
        check_insurance=True,
    )
    page.filling_field(value).should_show_calc(value).should_have_active_buttons(value)
@allure.epic("Ozon Deposit")
@allure.feature("Негативные сценарии")
@allure.story("Сумма ниже минимума")
@allure.tag('ui', 'deposit', 'negative', 'validation')
def test_deposit_invalid_sum_below_min():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount=9999
    )
    page.filling_field(value)
    page.should_have_stub()
@allure.epic("Ozon Deposit")
@allure.feature("Негативные сценарии")
@allure.story("Нечисловой ввод")
@allure.tag('ui', 'deposit', 'negative', 'validation')
def test_deposit_invalid_symbols():
    page = DepositPage().open_form()
    value = Deposit_class(
        deposit_amount="абвГДЕabcXYZ!@#$%^&*()",
    )
    page.filling_field(value)
    page.should_have_stub()
@allure.epic("Ozon Deposit")
@allure.feature("Отображение формы")
@allure.story("Форма отображается")
@allure.tag('ui', 'deposit', 'smoke')
def test_form_display_smoke():
    page = DepositPage().open_form()
    value = Deposit_class(deposit_amount=150000, term=3)
    page.filling_field(value).should_have_active_buttons()
    browser.element(L.RATE).should(be.visible)
    browser.element(L.PROFIT).should(be.visible)