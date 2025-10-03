
import allure
from selene import browser, be, have, query
from tests.pages.deposit_page import Deposit as DepositPage
from tests.models.deposit import Deposit_class
from tests.models.deposit_calculator_locators import DepositCalculatorLocators as L

@allure.epic("Ozon Deposit")
@allure.feature("Калькулятор вклада — дополнительные проверки")
class TestDepositExtra:
    @allure.story("Смена срока: 3 месяца — проверка типа вклада")
    @allure.severity(allure.severity_level.NORMAL)
    def test_term_3_months_updates_badge(self):
        page = DepositPage().open_form()
        value = Deposit_class(deposit_amount=150000, term=3, deposit_type="Вклад на 3 месяца")
        page.filling_field(value)
        browser.element(L.DEPOSIT_TYPE).should(be.visible).should(have.text("3"))

    @allure.story("Капитализация меняет расчёт прибыли (визуально)")
    @allure.severity(allure.severity_level.MINOR)
    def test_capitalization_toggles_profit_value(self):
        page = DepositPage().open_form()
        base = Deposit_class(deposit_amount=100000, term=4, check_capitalization=False)
        page.filling_field(base)
        profit_without = browser.element(L.PROFIT).get(query.text)

        with_cap = Deposit_class(deposit_amount=100000, term=4, check_capitalization=True)
        page.filling_field(with_cap)
        profit_with = browser.element(L.PROFIT).get(query.text)

        assert profit_without != profit_with, f"Ожидали различие прибыли при капитализации, получили одинаково: {profit_without}"
