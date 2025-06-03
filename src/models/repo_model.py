from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    id:int
    name:str
    description:str|None

    model_config = ConfigDict(from_attributes=True)

class Rent(BaseModel):
    id:int
    name:str
    description:str|None
    img:str|None
    price_id:int

    model_config = ConfigDict(from_attributes=True)

class Price(BaseModel):
    id:int
    month:int
    two_week:int
    day:int
    currency:str

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