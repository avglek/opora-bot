from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.dao.base import BaseDao
from src.dao.models import CategoryORM, RentORM, PriceORM, OrderORM, UserORM


class CategoryDao(BaseDao[CategoryORM]):
    model = CategoryORM

class RentDao(BaseDao[RentORM]):
    model = RentORM

    @classmethod
    async def get_by_category(cls, category_id: int,session:AsyncSession)->list[RentORM]:
        """
        Получить список аренд по категориям
        :param category_id: id категории
        :param session: сессия
        :return: список аренд по категории
        """

        query = select(CategoryORM).filter_by(id=category_id).options(selectinload(CategoryORM.rents))
        logger.info(f"Получение всех записей из БД {cls.model.__name__} для категории {category_id}")
        try:
            result = await session.execute(query)
            records = result.scalars().first().rents
            logger.info(f"Получено {len(records)} записей для категории {category_id} из БД {cls.model.__name__}")
            return records
        except Exception as ex:
            logger.error(f"Ошибка при получении аренды по категории {category_id} из БД {cls.model.__name__}: {ex}")
            raise

    @classmethod
    async def get_by_id_with_prices(cls,rent_id:int,session:AsyncSession)->RentORM|None:
        """
        Получить аренду по id с ценами
        :param rent_id: id аренды
        :param session: сессия
        :return: арендa по id с ценами по id
        """
        query = select(RentORM).filter_by(id=rent_id).options(selectinload(RentORM.price))
        logger.info(f"Получение аренды с ценами по id {rent_id} из БД {cls.model.__name__}")
        try:
            if rent_id:
                result = await session.execute(query)
                record = result.scalars().first()
                logger.info(f"Получена аренда с ценами по id {rent_id} из БД {cls.model.__name__}")
                return record
            else:
                return None
        except Exception as ex:
            logger.error(f"Ошибка при получении аренды с ценами по id {rent_id} из БД {cls.model.__name__}: {ex}")
            raise



class PriceDao(BaseDao[PriceORM]):
    model = PriceORM

class OrderDao(BaseDao[OrderORM]):
    model = OrderORM

class UserDao(BaseDao[UserORM]):
    model = UserORM