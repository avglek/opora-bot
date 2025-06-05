import asyncio
from datetime import datetime

from src.dao.dao import CategoryDao, PriceDao, RentDao, UserDao, OrderDao
from src.dao.database import connection
from src.dao.models import OrderORM, UserORM
from src.models.repo_model import User, Order
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


async def main() -> None:

    print('Starting...')

    order:Order = Order(
        user_id=1,
        rent_id=1,
        period_id=1,
        quantity=10,
        create_dt=datetime.now(),
    )


    print(order)

    id = await add_order(values=order)

    print(id)


if __name__ == "__main__":
    asyncio.run(main())