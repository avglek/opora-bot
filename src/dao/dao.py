from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.dao.base import BaseDao
from src.dao.models import Category, Rent, Price


class CategoryDao(BaseDao[Category]):
    model = Category

class RentDao(BaseDao[Rent]):
    model = Rent

    @classmethod
    async def get_by_category(cls, category_id: int,session:AsyncSession)->list[Rent]:
        """
        Получить список аренд по категориям
        :param category_id: id категории
        :param session: сессия
        :return: список аренд по категории
        """

        query = select(Category).filter_by(id=category_id).options(selectinload(Category.rents))
        logger.info(f"Получение всех записей из БД {cls.model.__name__} для категории {category_id}")
        try:
            result = await session.execute(query)
            records = result.scalars().first().rents
            logger.info(f"Получено {len(records)} записей для категории {category_id} из БД {cls.model.__name__}")
            return records
        except Exception as ex:
            logger.error(f"Ошибка при получении аренды по категории {category_id} из БД {cls.model.__name__}: {ex}")
            raise

class PriceDao(BaseDao[Price]):
    model = Price