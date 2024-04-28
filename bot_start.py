from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app_settings import tg_settings
from bot.handlers.commands import command_router
from bot.handlers.message import message_router
from bot.utils.settings.bot_settings import set_commands_for_bot, set_my_description_for_bot
import asyncio

import logging


async def start_bot():
    #Start bot

    quiz_battle_bot: Bot = Bot(tg_settings.token)
    memory_storage = MemoryStorage()
    dp_quiz_bot: Dispatcher = Dispatcher(bot=quiz_battle_bot, storage=memory_storage)

    #include routers
    dp_quiz_bot.include_routers(
        command_router,
        message_router
    )

    #set settings for bot
    await set_my_description_for_bot(bot=quiz_battle_bot)
    await set_commands_for_bot(bot=quiz_battle_bot)

    logging.basicConfig(level=logging.INFO)

    try:
        await dp_quiz_bot.start_polling(quiz_battle_bot)
    except KeyboardInterrupt as ky:
        logging.critical(msg="Бот завершил свою работу")
        await dp_quiz_bot.stop_polling()


if __name__ == "__main__":
    asyncio.run(start_bot())