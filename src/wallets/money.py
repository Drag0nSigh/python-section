from dataclasses import dataclass
from typing import Any

from src.wallets.currency import Currency
from src.wallets.exceptions import NegativeValueException, NotComparisonException


@dataclass
class Money:
    value: float
    currency: Currency

    def __init__(self, value: float, currency: Currency):
        if value < 0:
            raise NegativeValueException()
        self.value = value
        self.currency = currency

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise NotComparisonException()
        result = self.value + other.value
        if result < 0:
            raise NegativeValueException()
        return Money(value=result, currency=self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise NotComparisonException()
        result = self.value - other.value
        if result < 0:
            raise NegativeValueException()
        return Money(value=result, currency=self.currency)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            return False
        return self.value == other.value and self.currency == other.currency


class Wallet:
    def __init__(self, *moneys: Money):
        self._balances: dict[Currency, Money] = {}
        for money in moneys:
            if money.value < 0:
                raise NegativeValueException()
            self._balances[money.currency] = money

    def __getitem__(self, currency: Currency) -> Money:
        return self._balances.get(currency, Money(value=0, currency=currency))

    def __delitem__(self, currency: Currency) -> None:
        self._balances.pop(currency, None)

    def __len__(self) -> int:
        return len(self._balances)

    def __contains__(self, currency: Currency) -> bool:
        return currency in self._balances

    def add(self, money: Money) -> 'Wallet':
        if money.value < 0:
            raise NegativeValueException()
        current = self[money.currency]
        self._balances[money.currency] = current + money
        return self

    def sub(self, money: Money) -> 'Wallet':
        if money.value < 0:
            raise NegativeValueException()
        result = self[money.currency] - money
        if result.value < 0:
            raise NegativeValueException()
        self._balances[money.currency] = result
        return self

    @property
    def currencies(self) -> set[Currency]:
        return set(self._balances.keys())
