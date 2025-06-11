from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, Mapped, joinedload

from src.dao.base import BaseDao
from src.dao.models import CategoryORM, RentORM, PriceORM, OrderORM, UserORM
from src.models.repo_model import User


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

        query = select(CategoryORM).filter_by(id=category_id).options(selectinload(CategoryORM.rents).options(selectinload(RentORM.price)))
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

    @classmethod
    async def get_all_by_user(cls,user_id:int,session:AsyncSession)-> list[OrderORM]|None:
        if user_id and session:
            query = (select(OrderORM)
                     .filter_by(user_id=user_id)
                     .options(joinedload(OrderORM.rent).options(joinedload(RentORM.price))))
            logger.info(f"Получение всех записей из БД {cls.model.__name__} для пользователя {user_id}")
            try:
                result = await session.execute(query)
                records = result.scalars().all()
                logger.info(f"Получено {len(records)} записей для пользователя {user_id} из БД {cls.model.__name__}")
                if not records:
                    return None
                return records
            except Exception as ex:
                    logger.error(f"Ошибка при получении заказов пользователя {user_id} из БД {cls.model.__name__}: {ex}")
                    raise



class UserDao(BaseDao[UserORM]):
    model = UserORM

    @classmethod
    async def get_user_by_telegram_id(cls,telegram_id:int,session:AsyncSession)->User|None:
        """
        Получить пользователя по telegram_id
        :param telegram_id: telegram_id пользователя
        :param session: сессия
        :return: пользователь по telegram_id
        """
        if telegram_id and session:
            query = select(UserORM).filter_by(telegram_id=telegram_id)
            logger.info(f"Получение пользователя по telegram_id {telegram_id} из БД {cls.model.__name__}")
            try:
                result = await session.execute(query)
                record = result.scalars().first()
                if not record:
                    logger.info(f"Пользователь по telegram_id {telegram_id} не найден в БД {cls.model.__name__}")
                    return None
                logger.info(f"Получен пользователь по telegram_id {telegram_id} из БД {cls.model.__name__}")
                return User.model_validate(record)
            except Exception as ex:
                logger.error(f"Ошибка при получении пользователя по telegram_id {telegram_id} из БД {cls.model.__name__}: {ex}")
                raise
        else:
            if not telegram_id:
                logger.error(f"telegram_id не передан")
                raise ValueError("telegram_id не передан")
            elif not session:
                logger.error(f"Сессия не передана")
                raise ValueError("Сессия не передана")
