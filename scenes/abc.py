from aiogram import types

from scene_manager import MessageScene
from scene_manager.scenes.filters import context_type_filter


class Test(MessageScene):
    @context_type_filter(['voice', 'text'])
    async def home(self, message: types.Message):
        await message.reply("It`s work")
        await self.set_scene(message, "start")

    async def start(self, message: types.Message):
        await message.reply("start")
        await self.set_scene(message, "start2")

    class Config:
        content_types = 'text'
        otherwise_handler = None
