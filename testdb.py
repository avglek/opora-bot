import asyncio
from datetime import datetime

from src.dao.dao import CategoryDao, PriceDao, RentDao, UserDao, OrderDao
from src.dao.database import connection
from src.dao.models import OrderORM, UserORM
from src.models.repo_model import User, Order, OrderInfo
from src.services.repo import Repo


@connection
async def get_categories(session, **kwargs) -> list:
    return await CategoryDao.get_all(session=session, **kwargs)

@connection
async def add_user(session, **kwargs):
    print(kwargs)
    user = await UserDao.add(session=session, **kwargs)
    id = user.id
    await session.commit()
    return id

#{'rent_id': '1', 'period_id': '1', 'quantity': 10}
@connection
async def add_order(session, **kwargs):
    print(kwargs)
    order = await OrderDao.add(session=session, **kwargs)
    id = order.id
    await session.commit()
    return id

@connection
async def get_orders(session, **kwargs):
    return await Repo.get_all_orders(session=session, **kwargs)

@connection
async def get_order_info(session, **kwargs):
    return await Repo.get_order_info(session=session, **kwargs)

@connection
async def get_rents(session, **kwargs):
    return await Repo.get_rents_by_category(session=session, **kwargs)


#{'quantity': 8, 'period_id': 2, 'rent_id': 8, 'user_id': 1}
async def main() -> None:

    print('Starting...')

    orders = await get_orders(user_id=1)

    info = list()
    for order in orders:
        info.append(order)

    for i in info:
        print(i)




if __name__ == "__main__":
    asyncio.run(main())