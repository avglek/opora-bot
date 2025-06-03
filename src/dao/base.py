from typing import TypeVar, Generic, List

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func

from src.dao.database import Base

# Объявляем типовой параметр T с ограничением, что это наследник Base
T = TypeVar("T", bound=Base)

class BaseDao(Generic[T]):
    model: type[T]

    @classmethod
    async def get_all(cls,session:AsyncSession,filters:BaseModel|None=None) -> list[T]:
        """
        Получение всех записей из БД
        :param session: сессия базы данных
        :param filters: фильтры поиска
        :return: список записей
        """
        filter_dict=filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f"Получение всех записей из БД {cls.model.__name__} с фильтрами {filters}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Получено {len(records)} записей из БД {cls.model.__name__}")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении записей из БД {cls.model.__name__}: {e}")
            raise

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession)-> T|None:
        """
        Найти запись по ID
        :param session: сессия базы данных
        :param data_id: ID записи: int
        :return: запись или None
        """
        logger.info(f"Поиск {cls.model.__name__} с ID: {data_id}")
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись с ID {data_id} найдена.")
            else:
                logger.info(f"Запись с ID {data_id} не найдена.")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {data_id}: {e}")
            raise

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel)->T|None:
        """
        Найти одну запись по фильтрам
        :param session: сессия базы данных
        :param filters: фильтры поиска
        :return: найденная запись или None
        """
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Поиск одной записи {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись найдена по фильтрам: {filter_dict}")
            else:
                logger.info(f"Запись не найдена по фильтрам: {filter_dict}")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
            raise

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel)->T:
        """
        Добавить одну запись
        :param session: сессия базы данных
        :param values: значения для добавления
        :return: добавленная запись
        """
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Добавление записи {cls.model.__name__} с параметрами: {values_dict}")
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
            logger.info(f"Запись {cls.model.__name__} успешно добавлена.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel])->list[T]:
        """
        Добавить несколько записей
        :param session: сессия базы данных
        :param instances: список записей
        :return: список добавленных записей
        """
        values_list = [item.model_dump(exclude_unset=True) for item in instances]
        logger.info(f"Добавление нескольких записей {cls.model.__name__}. Количество: {len(values_list)}")
        new_instances = [cls.model(**values) for values in values_list]
        session.add_all(new_instances)
        try:
            await session.flush()
            logger.info(f"Успешно добавлено {len(new_instances)} записей.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении нескольких записей: {e}")
            raise e
        return new_instances

    @classmethod
    async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel)->int:
        """
        Обновить записи по фильтрам
        :param session: сессия базы данных
        :param filters: фильтры поиска
        :param values: значения для обновления
        :return: количество обновленных записей
        """
        filter_dict = filters.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Обновление записей {cls.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}")
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_dict.items()])
            .values(**values_dict)
            .execution_options(synchronize_session="fetch")
        )
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Обновлено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при обновлении записей: {e}")
            raise e

    @classmethod
    async def delete(cls, session: AsyncSession, filters: BaseModel)->int:
        """
        Удалить записи по фильтрам
        :param session: сессия базы данных
        :param filters: фильтры поиска
        :return: количество удаленных записей
        """
        filter_dict = filters.model_dump(exclude_unset=True)
        logger.info(f"Удаление записей {cls.model.__name__} по фильтру: {filter_dict}")
        if not filter_dict:
            logger.error("Нужен хотя бы один фильтр для удаления.")
            raise ValueError("Нужен хотя бы один фильтр для удаления.")

        query = sqlalchemy_delete(cls.model).filter_by(**filter_dict)
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Удалено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при удалении записей: {e}")
            raise e

    @classmethod
    async def count(cls, session: AsyncSession, filters: BaseModel | None = None)->int:
        """
        Подсчитать количество записей
        :param session: сессия базы данных
        :param filters: фильтры поиска
        :return: количество записей
        """
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logger.info(f"Подсчет количества записей {cls.model.__name__} по фильтру: {filter_dict}")
        try:
            query = select(func.count(cls.model.id)).filter_by(**filter_dict)
            result = await session.execute(query)
            count = result.scalar()
            logger.info(f"Найдено {count} записей.")
            return count
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подсчете записей: {e}")
            raise