from dataclasses import dataclass
from typing import Any, Type, Coroutine
from unicodedata import category

from sqlalchemy import select
from sqlalchemy.orm import Session
import src.models.rent_models as models


@dataclass
class Category:
    id:int
    name:str
    description:str

@dataclass
class Rent:
    id:int
    name:str
    description:str
    img:str
    price_id:str

@dataclass
class Prise:
    id:int
    month:int
    two_week:int
    day:int
    currency:str

class Repo:

    def __init__(self,session:Session) -> None:
        self.session = session

    def get_categories(self) -> dict[str, tuple[str, int]]:
        if self.session:
            stm = select(models.Category)
            rows = self.session.execute(stm).all()
            result = {'categories': []}
            for row in rows:
                result['categories'].append((row.Category.name, row.Category.id))
            return result

        else:
            return []

