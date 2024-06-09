from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class Currency(Enum):
    RUB = "SUR"


class Issuer:
    inn: str
    name: str


class Bond:
    isin: str
    name: str
    issuer: Issuer
    nominal_price: Decimal
    currency: Currency
    coupon_rate: Decimal
    current_price_percent: Decimal
    payments_interval: int
    maturity_date: datetime
    offer_date: datetime
    buy_back_date: datetime
    buy_back_price: Decimal

    def __init__(self,
                 isin: str,
                 name: str = None,
                 issuer: Optional[Issuer] = None,
                 nominal_price: Optional[Decimal] = None,
                 currency: Optional[Currency] = None,
                 coupon_rate: Optional[Decimal] = None,
                 current_price_percent: Optional[Decimal] = None,
                 payments_interval: Optional[int] = None,
                 maturity_date: Optional[datetime] = None,
                 board_id: Optional[str] = None,
                 offer_date: Optional[datetime] = None,
                 buy_back_date: Optional[datetime] = None,
                 buy_back_price: Optional[Decimal] = None,):
        self.isin = isin
        self.name = name
        self.issuer = issuer
        self.nominal_price = nominal_price
        self.currency = currency
        self.coupon_rate = coupon_rate
        self.current_price_percent = current_price_percent
        self.payments_interval = payments_interval
        self.maturity_date = maturity_date
        self.board_id = board_id
        self.offer_date = offer_date
        self.buy_back_date = buy_back_date
        self.buy_back_price = buy_back_price

    def __repr__(self):
        return f"Bond {self.isin}"