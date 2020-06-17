from aiogram import types

from scene_manager import MessageScene, CallbackQueryScene
from scene_manager import filters


class Test(MessageScene):
    @filters.context_types_filter(['voice', 'text'])
    async def home(self, message: types.Message):
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton('👍', callback_data="111111"),
            types.InlineKeyboardButton('👎', callback_data="111211"),
        )
        await message.reply('Posts', reply_markup=markup)
        await self.set_scene(message, "start")

    async def start(self, message: types.Message):
        await message.reply("start")
        await self.set_scene(message, "start2")

    class Config:
        content_types = ['text']
        otherwise_handler = None


class Test2(CallbackQueryScene):
    @filters.query_data_filter(["111111"])
    async def start(self, query: types.CallbackQuery):
        await query.message.edit_text('agagagagag')
        await self.set_scene(query, "start2")
