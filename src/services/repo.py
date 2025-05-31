from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import Session
import src.models.rent_models as models
from src.lexicon.lexicon_ru import PRICE_PERIOD


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
class Price:
    id:int
    month:int
    two_week:int
    day:int
    currency:str

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

class Repo:

    def __init__(self,session:Session) -> None:
        self.session = session

    async def get_rents_by_category(self, category_id)->list[Rent]:
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

    async def get_all_categories(self)->list[Category]:
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

    async def get_rent_by_id(self,rent_id)->Rent|None:
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

    async def get_price_info_by_id(self,price_id)->list[PriceInfo]|None:
        if self.session:
            stm = select(models.Price).where(models.Price.id == price_id)
            row = self.session.execute(stm).all()
            price = Price(
                row[0].Price.id,
                row[0].Price.month,
                row[0].Price.two_week,
                row[0].Price.day,
                row[0].Price.currency
            )

            result = [
                PriceInfo(1,PRICE_PERIOD['month'],price.month,price.currency),
                PriceInfo(2,PRICE_PERIOD['two_week'],price.two_week,price.currency),
                PriceInfo(3,PRICE_PERIOD['day'],price.day,price.currency)
            ]
            return result
        else:
            return None

    async def get_order_info(self,rent_id,price_id,period_id)->OrderInfo|None:
        print(f'rent_id:{rent_id},price_id:{price_id},period_id:{period_id}')
        if self.session:
            stm_rent = select(models.Rent).where(models.Rent.id == rent_id)
            stm_price = select(models.Price).where(models.Price.id == price_id)
            row_rent = self.session.execute(stm_rent).all()
            row_price = self.session.execute(stm_price).all()

            rent_name = row_rent[0].Rent.name

            price = Price(
                row_price[0].Price.id,
                row_price[0].Price.month,
                row_price[0].Price.two_week,
                row_price[0].Price.day,
                row_price[0].Price.currency
            )
            price_info = 0,
            period = ''

            match period_id:
                case 1:
                    price_info = price.month
                    period = 'month'
                case 2:
                    price_info = price.two_week
                    period = 'two_week'
                case 3:
                    price_info = price.day
                    period = 'day'

            period_ru = PRICE_PERIOD[period]


            return OrderInfo(rent_name,period,period_ru,price_info,price.currency)
        else:
            return None

