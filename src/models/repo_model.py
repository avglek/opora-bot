from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    id:int|None = None
    name:str
    description:str|None = None

    model_config = ConfigDict(from_attributes=True)

class Price(BaseModel):
    id: int | None = None
    month: int
    two_week: int | None = None
    day: int | None = None
    currency: str | None = None

    model_config = ConfigDict(from_attributes=True)

class Rent(BaseModel):
    id:int|None = None
    name:str
    description:str|None = None
    img:str
    price_id:int|None = None
    price:Price|None = None

    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    id:int|None = None
    number:str|None = None
    quantity:int
    period_id:int
    summa:int|None = None
    rent_id:int|None = None
    rent:Rent|None = None
    user_id:int|None = None
    create_dt:datetime|None = None
    accept_dt:datetime|None = None
    close_dt:datetime|None = None

    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id:int|None = None
    name:str
    email:str|None = None
    firstname:str|None = None
    lastname:str|None = None
    telegram_id:int

    model_config = ConfigDict(from_attributes=True)

@dataclass
class PriceInfo:
    id:int
    period:str
    price:int
    currency:str

@dataclass
class OrderInfo:
    rent_name:str
    period:str
    period_ru:str
    price:int
    currency:str


