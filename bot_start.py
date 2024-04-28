from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app_settings import tg_settings
from bot.handlers.commands import command_router
import asyncio

import logging


async def start_bot():
    #Start bot

    print(tg_settings.token)
    quiz_battle_bot: Bot = Bot(tg_settings.token)
    memory_storage = MemoryStorage()
    dp_quiz_bot: Dispatcher = Dispatcher(bot=quiz_battle_bot, storage=memory_storage)

    #include routers
    dp_quiz_bot.include_router(
        command_router
    )

    logging.basicConfig(level=logging.INFO)

    try:
        await dp_quiz_bot.start_polling(quiz_battle_bot)
    except KeyboardInterrupt as ky:
        logging.critical(msg="Бот завершил свою работу")
        await dp_quiz_bot.stop_polling()


if __name__ == "__main__":
    asyncio.run(start_bot())