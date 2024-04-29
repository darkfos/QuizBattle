from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app_settings import tg_settings
from bot.handlers.commands import command_router
from bot.handlers.message import message_router
from bot.handlers.state_router import state_router
from bot.utils.settings.bot_settings import set_commands_for_bot, set_my_description_for_bot
from typing import Any, Dict, Callable, Awaitable
from bot.req_api.user_api import UserApi, AddNewUserPDSchema
from datetime import datetime
from aiogram.types import Update, Message, CallbackQuery
from bot.middleware.AuthUser import AuthUserMiddleware
import asyncio

import logging

quiz_battle_bot: Bot = Bot(tg_settings.token)
memory_storage = MemoryStorage()
dp_quiz_bot: Dispatcher = Dispatcher(bot=quiz_battle_bot, storage=memory_storage)


async def start_bot():
    #Start bot

    #include routers
    dp_quiz_bot.include_routers(
        command_router,
        state_router,
        message_router
    )

    #set settings for bot
    await set_my_description_for_bot(bot=quiz_battle_bot)
    await set_commands_for_bot(bot=quiz_battle_bot)

    #Added middleware
    dp_quiz_bot.message.middleware.register(AuthUserMiddleware())

    logging.basicConfig(level=logging.INFO)

    try:
        await dp_quiz_bot.start_polling(quiz_battle_bot)
    except KeyboardInterrupt as ky:
        logging.critical(msg="Бот завершил свою работу")
        await dp_quiz_bot.stop_polling()

#middleware for updates
@dp_quiz_bot.update.outer_middleware()
async def database_transaction_middleware(
    handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: Dict[str, Any]
) -> Any:
    
    user_api: UserApi = UserApi()

    if event.callback_query is not None:
        user_is_created: bool = await user_api.register_user(
                user_data=AddNewUserPDSchema(
                    name_user=event.callback_query.from_user.first_name,
                    score=0,
                    game_count=0,
                    date_create=datetime.now().date(),
                    date_update=datetime.now().date(),
                    telegram_id=int(event.callback_query.from_user.id)
                )
            )

        if user_is_created:
            if isinstance(event, Message):
                await event.answer(
                    text="🔒 Сработала система безопасности, вы ещё не зарегистрированы в системе, сейчас подправим..."
                )
            elif isinstance(event, CallbackQuery):
                await event.answer()
            await user_api.create_access_token(telegram_id=event.callback_query.from_user.id)
            return await handler(event, data)
        else:
            await user_api.create_access_token(telegram_id=event.callback_query.from_user.id)
            return await handler(event, data)
    return await handler(event, data)


if __name__ == "__main__":
    asyncio.run(start_bot())