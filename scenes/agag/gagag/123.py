from aiogram import types

from scene_manager import MessageScene


class Test2(MessageScene):
    async def start2(self, message: types.Message):
        await message.reply("start2")
        await self.set_scene(message, "start3")

    async def start3(self, message: types.Message):
        await message.reply("start3")
        await self.set_scene(message, "home")
