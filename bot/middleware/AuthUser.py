from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery, Update
from typing import Any, Callable, Dict, Awaitable, Union
from api.backend.schemas.UserPDSchema import AddNewUserPDSchema
from bot.req_api.user_api import UserApi
from datetime import datetime

class AuthUserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery, Update], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery, InlineQuery, Update],
            data: Dict[str, Any]
    ) -> Any:
        
        user_api: UserApi = UserApi()

        user_is_created: bool = await user_api.register_user(
            user_data=AddNewUserPDSchema(
                name_user=event.from_user.first_name,
                score=0,
                game_count=0,
                date_create=datetime.now().date(),
                date_update=datetime.now().date(),
                telegram_id=int(event.from_user.id)
            )
        )

        if user_is_created:
            if isinstance(event, Message):
                await event.answer(
                    text="🔒 Сработала система безопасности, вы ещё не зарегистрированы в системе, сейчас подправим..."
                )
            elif isinstance(event, CallbackQuery):
                await event.answer()
            await user_api.create_access_token(telegram_id=event.from_user.id)
            return await handler(event, data)
        else:
            await user_api.create_access_token(telegram_id=event.from_user.id)
            return await handler(event, data)
