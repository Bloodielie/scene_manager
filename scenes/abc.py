from aiogram import types

from scene_manager import MessageScene


class Test(MessageScene):
    async def home(self, message: types.Message):
        await message.reply("It`s work")
        await self.set_scene(message, "start")

    async def start(self, message: types.Message):
        await message.reply("start")
        await self.set_scene(message, "start2")
