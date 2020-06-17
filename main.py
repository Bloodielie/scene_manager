import logging

from aiogram import Bot, Dispatcher, executor
from loguru import logger

from scene_manager import Manager

API_TOKEN = '1044634890:AAH-SPNadtR2lOubfQAfyPAfbyOgf2wIyms'
logger.remove()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
manager = Manager(dispatcher=dp)

if __name__ == '__main__':
    manager.register_handlers()
    executor.start_polling(dp, skip_updates=True)
