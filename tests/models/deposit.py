from dataclasses import dataclass
from typing import Optional

@dataclass
class Deposit_class:
    deposit_amount: Optional[str] = None
    term: Optional[str] = None
    interest_rate: Optional[str] = None
    profit_amount: Optional[str] = None
    deposit_type: Optional[str] = None
    day: Optional[int] = None
    month: Optional[str] = None
    year: Optional[int] = None

    check_capitalization: bool = False
    check_insurance: bool = False
    check_conditions: bool = False
    check_cta: bool = False

    @property
    def maturity_date(self) -> str:
        if self.day and self.month and self.year:
            return f"{int(self.day):02d} {self.month} {self.year}"
        return ""
