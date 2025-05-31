import asyncio
from typing import List, Any, Coroutine

from sqlalchemy.orm import Session

from config import Config, load_config
from sqlalchemy import create_engine

from src.lexicon.lexicon_ru import PRICE_PERIOD
from src.models.rent_models import Category
from src.services.repo import Repo

config:Config = load_config()
print(f"Test db {config.db.get_local_url()}")

engine = create_engine(config.db.get_local_url(), echo=False)
session = Session(engine)

repo = Repo(session)

#{'rent_id': '6', 'price_id': 4, 'period_id': '2'}
#rent_id:7,price_id:2,period_id:1

async def main() -> None:
    print(await repo.get_order_info(
        rent_id=7,
        price_id=2,
        period_id=1))

if __name__ == "__main__":
    asyncio.run(main())