import logging

from aiogram import Bot, Dispatcher, executor, types
from scene_manager import Manager
from aiogram.types import ContentType

API_TOKEN = '1044634890:AAH-SPNadtR2lOubfQAfyPAfbyOgf2wIyms'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
manager = Manager(dispatcher=dp)


# @dp.message_handler(content_types=['video', 'text', 'document'])
# async def agagaga(message: types.Message):
#     """
#     This handler will be called when user sends `/start` or `/help` command
#     """
#     print(isinstance(message.content_type, str))
#     await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


if __name__ == '__main__':
    manager.register_handlers()
    executor.start_polling(dp, skip_updates=True)
