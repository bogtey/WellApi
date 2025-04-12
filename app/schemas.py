from pydantic import BaseModel
from datetime import date

class CurrencyRateBase(BaseModel):
    currency_code: str
    currency_name: str
    value: float
    date: date

class CurrencyRateCreate(CurrencyRateBase):
    pass

class CurrencyRate(CurrencyRateBase):
    id: int

    class Config:
        orm_mode = True