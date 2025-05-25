from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.services.repo import Repo


class CustomMiddleware(BaseMiddleware):
    def __init__(self,repo:Repo):
        self._name = "CustomMiddleware"
        self._repo = repo

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        print("self",self)
        data["repo"] = self._repo
        return await handler(event, data)