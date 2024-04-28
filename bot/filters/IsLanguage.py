from aiogram.filters import BaseFilter
from aiogram import types


class IsGameModeFilter(BaseFilter):

    async def __call__(
        self,
        message: types.Message
    ) -> bool:
        
        if message.text in ("👑 Мастер перевода", "📝 Скоростной букварь", "💡 Обратный перевод"):
            return True
        else:
            return False
        

class IsLanguageFilter(BaseFilter):

    async def __call__(
        self,
        message: types.CallbackQuery
    ) -> bool:

        if message.data.endswith("_gmt"):
            return True
        else:
            return False