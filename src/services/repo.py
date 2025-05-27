from dataclasses import dataclass
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

    async def get_rents_by_category(self, category_id):
        if self.session:
            stm = select(models.Category).where(models.Category.id == category_id)
            rows = self.session.execute(stm).all()

            result = list()
            for rent in rows[0].Category.rents:
                item = Rent(rent.id,rent.name,rent.description,rent.img,rent.price_id)
                result.append(item)

            return result

        else:
            result = []
        return result

    async def get_all_categories(self):
        if self.session:
            stm = select(models.Category)
            rows = self.session.execute(stm).all()

            result = list()
            for row in rows:
                item = Category(row.Category.id,row.Category.name,row.Category.description)
                result.append(item)
            return result
        else:
            return []

    async def get_rent_by_id(self,rent_id):
        if self.session:
            stm = select(models.Rent).where(models.Rent.id == rent_id)
            row = self.session.execute(stm).all()
            result = Rent(
                row[0].Rent.id,
                row[0].Rent.name,
                row[0].Rent.description,
                row[0].Rent.img,
                row[0].Rent.price_id)
            return result
        else:
            return None


