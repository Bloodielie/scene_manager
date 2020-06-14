from aiogram import types

from scene_manager import MessageScene


class Test(MessageScene):
    async def home(self, message: types.Message):
        await message.reply("It`s work")
        await self.change_scene(message, "start")

    async def start(self, message: types.Message):
        await message.reply("start")
        await self.change_scene(message, "home")
