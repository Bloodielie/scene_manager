from aiogram import Dispatcher
from scene_manager.storages.base import BaseStorage
from aiogram.types.base import TelegramObject


class BaseScene:
    def __init__(self, dispatcher: Dispatcher, storage: BaseStorage) -> None:
        self.dispatcher = dispatcher
        self.storage = storage
        self.bot = self.dispatcher.bot
        
    async def set_scene(self, ctx: TelegramObject, scene_name: str) -> None:
        await self.storage.put(ctx.from_user.id, scene_name)


class MessageScene(BaseScene):
    pass


class QueryScene(BaseScene):
    pass
