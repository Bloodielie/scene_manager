import logging

from aiogram import Bot, Dispatcher, executor, types
from loguru import logger

from scene_manager.middleware import ScenesMiddleware

API_TOKEN = '1044634890:AAH-SPNadtR2lOubfQAfyPAfbyOgf2wIyms'
logger.remove()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(ScenesMiddleware())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
