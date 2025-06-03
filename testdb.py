import asyncio

from src.dao.dao import CategoryDao, PriceDao, RentDao
from src.dao.database import connection


@connection
async def get_categories(session, **kwargs) -> list:
    return await CategoryDao.get_all(session=session, **kwargs)

@connection
async def get_rents_by_cat_id(session, **kwargs) -> list:
    return await RentDao.get_by_category(session=session, **kwargs)



async def main() -> None:
    #print(await get_categories())
    print(await get_rents_by_cat_id(category_id=4))

if __name__ == "__main__":
    asyncio.run(main())