from sqlalchemy import Column, Integer, String, Numeric, Date
from .database import Base

class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)
    currency_code = Column(String(3), index=True)
    currency_name = Column(String(50))
    value = Column(Numeric)
    date = Column(Date)