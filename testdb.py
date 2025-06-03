import asyncio

from src.dao.dao import CategoryDao, PriceDao, RentDao
from src.dao.database import connection
from src.services.repo import Repo


@connection
async def get_categories(session, **kwargs) -> list:
    return await CategoryDao.get_all(session=session, **kwargs)

@connection
async def get_order_info(session, **kwargs) -> list:
    return await Repo.get_order_info(session=session, **kwargs)



async def main() -> None:

    print(await get_order_info(rent_id=1,period_id=1))

if __name__ == "__main__":
    asyncio.run(main())