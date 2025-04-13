from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def fetch_currency_rates():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status() 
            root = ET.fromstring(response.text)
            date_str = root.attrib['Date']
            date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()

            with SessionLocal() as db:  
                for valute in root.findall('Valute'):
                    currency_code = valute.find('CharCode').text
                    currency_name = valute.find('Name').text
                    value = float(valute.find('Value').text.replace(',', '.'))

                    currency_rate = schemas.CurrencyRateCreate(
                        currency_code=currency_code,
                        currency_name=currency_name,
                        value=value,
                        date=date_obj
                    )

                    db_currency_rate = models.CurrencyRate(**currency_rate.dict())
                    db.add(db_currency_rate)
                db.commit()
        except httpx.HTTPStatusError as e:
            print(f"Ошибка HTTP: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

@app.on_event("startup")
async def startup_event():
    await fetch_currency_rates() 

@app.get("/")
async def read_root(db: Session = Depends(get_db)):
    currency_rates = db.query(models.CurrencyRate).all() 
    return currency_rates

@app.get("/currency_rates/", response_model=list[schemas.CurrencyRate])
def read_currency_rates(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    currency_rates = db.query(models.CurrencyRate).offset(skip).limit(limit).all()
    return currency_rates
