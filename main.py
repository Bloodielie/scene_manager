import logging

from aiogram import Bot, Dispatcher, executor
from loguru import logger

from scene_manager.loader.loader import Loader
from scene_manager.middleware import ScenesMiddleware

API_TOKEN = '1044634890:AAH-SPNadtR2lOubfQAfyPAfbyOgf2wIyms'
logger.remove()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
loader = Loader(dp)
dp.middleware.setup(ScenesMiddleware())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
