from selene import by

class DepositCalculatorLocators:
    AMOUNT   = by.css('input[data-testid="deposit-landing-money-input"]')
    TERM_BTN = lambda months: by.xpath(
        f"//div[@data-testid='radio-group-button']//div[contains(@class,'content') and normalize-space()='{months} мес']"
    )
    RATE     = by.xpath("(//div[@data-testid='interest-rate']//span)[1]")
    PROFIT   = by.xpath("//div[@data-testid='income']")
    MATURITY = by.xpath("//div[@data-testid='income']//span")
    CTA      = by.xpath("(//button[contains(., 'Открыть') and contains(., 'вклад') and contains(., 'бесплатно')])[2]")
    CONDITIONS = by.xpath("//a[@data-testid='rates-button']")
    DEPOSIT_TYPE = by.xpath("//div[@data-testid='ob-badge']")

    CAPITALIZATION = by.xpath("//div[@data-testid='capitalization']")
    INSURANCE = by.xpath("// div[normalize - space(.)='Средства на вкладе застрахованы']")

