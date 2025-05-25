import asyncio
from typing import List, Any, Coroutine

from sqlalchemy.orm import Session

from config import Config, load_config
from sqlalchemy import create_engine

from src.models.rent_models import Category
from src.services.repo import Repo

config:Config = load_config()
print(f"Test db {config.db.get_local_url()}")

engine = create_engine(config.db.get_local_url(), echo=True)
session = Session(engine)

repo = Repo()

async def main() -> None:
    print(await get_categories(session))

if __name__ == "__main__":
    asyncio.run(main())