from aiogram.filters import BaseFilter
from aiogram import types


class DeleteProfile(BaseFilter):


    async def __call__(
        self,
        clb: types.CallbackQuery
    ) -> bool:
        
        if clb.data.endswith("del"): return True
        else: return False