from dataclasses import dataclass

@dataclass
class Deposit_class:
    deposit_amount: int = None
    term: int = None
    interest_rate: str = None
    profit_amount: str = None
    day: int = None
    month: str = None
    year: int = None
    deposit_type: str = None

    @property
    def maturity_date(self) -> str:
        return f'{int(self.day):02d} {self.month} {self.year}'
