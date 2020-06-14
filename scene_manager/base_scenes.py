from typing import Optional, Union

from aiogram import Dispatcher
from scene_manager.storages.base import BaseStorage
from aiogram.types.base import TelegramObject
from aiogram.types.message import ContentType


class BaseScene:
    def __init__(self, dispatcher: Dispatcher, storage: BaseStorage) -> None:
        self.dispatcher = dispatcher
        self.storage = storage
        self.bot = self.dispatcher.bot
        
    async def set_scene(self, ctx: TelegramObject, scene_name: str) -> None:
        await self.storage.put(ctx.from_user.id, scene_name)


class MessageScene(BaseScene):
    # todo: внедрить наработки из test.py
    class Config:
        content_types: Optional[Union[ContentType, str]] = None


class QueryScene(BaseScene):
    pass
