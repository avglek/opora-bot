from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.dao import CategoryDao, RentDao, PriceDao, OrderDao
from src.lexicon.lexicon_ru import PRICE_PERIOD
from src.models.repo_model import Category, Rent, PriceInfo, OrderInfo, Order


class Repo:

    @staticmethod
    async def get_rents_by_category(category_id:int, session: AsyncSession)->list[Rent]:
        if session:

            result = list()
            rows = await RentDao.get_by_category(category_id=category_id,session=session)
            for row in rows:
                item = Rent.model_validate(row)
                result.append(item)

            return result

        else:
            result = []
        return result

    @staticmethod
    async def get_all_categories(session: AsyncSession)->list[Category]:
        if session:
            categories = await CategoryDao.get_all(session=session)

            result = list()
            for category in categories:
                item = Category.model_validate(category)
                result.append(item)
            return result
        else:
            return []

    @staticmethod
    async def get_rent_by_id(rent_id:int, session: AsyncSession)->Rent|None:
        if session:
            row = await RentDao.find_one_or_none_by_id(data_id=rent_id,session=session)
            return Rent.model_validate(row)
        else:
            return None

    @staticmethod
    async def get_price_info_by_id(price_id:int,session: AsyncSession)->list[PriceInfo]|None:
        if session:
            price = await PriceDao.find_one_or_none_by_id(data_id=price_id,session=session)

            if price:
                result = [
                    PriceInfo(1,PRICE_PERIOD['month'],price.month,price.currency),
                    PriceInfo(2,PRICE_PERIOD['two_week'],price.two_week,price.currency),
                    PriceInfo(3,PRICE_PERIOD['day'],price.day,price.currency)
                ]
                return result
        else:
            return None

    @staticmethod
    async def get_order_info(rent_id:int,period_id:int,session: AsyncSession)->OrderInfo|None:

        if session:
            rent:Rent|None = await RentDao.get_by_id_with_prices(rent_id=rent_id,session=session)

            price_info = 0,
            period = ''

            match period_id:
                case '1':
                    price_info = rent.price.month
                    period = 'month'
                case '2':
                    price_info = rent.price.two_week
                    period = 'two_week'
                case '3':
                    price_info = rent.price.day
                    period = 'day'

            return OrderInfo(rent.name,period,PRICE_PERIOD[period],price_info,rent.price.currency)
        else:
            return None

    @staticmethod
    async def get_all_orders(session: AsyncSession)->list[OrderInfo]:
        if session:
            orders = await OrderDao.get_all(session=session)

            result = list()
            for order in orders:
                item = Order.model_validate(order)
                result.append(item)

            return result
        else:
            return []

    @staticmethod
    async def add_order(order:Order,session: AsyncSession)->bool:
        if session:
            await OrderDao.add(values=order,session=session)
            return True
        else:
            return False

