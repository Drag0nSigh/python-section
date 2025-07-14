from dataclasses import dataclass


@dataclass(frozen=True)
class Currency:
    code: str


rub = Currency(code="RUB")
usd = Currency(code="USD")
