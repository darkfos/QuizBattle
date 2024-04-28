from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from bot.utils.text.command_text import (text_for_start_command,
                                        text_for_help_command,
                                        text_for_profile)

from bot.key.inln_kb import btn_for_profile


command_router: Router = Router()


@command_router.message(CommandStart())
async def start_command(message: types.Message) -> None:
    """
    Start command bot
    """

    message_for_user: str = "".join(await text_for_start_command(username=message.from_user.username))

    await message.answer_animation(
        animation=FSInputFile("bot/static/start.gif"),
        caption=message_for_user,
        parse_mode=ParseMode.HTML
    )


@command_router.message(Command("help"))
async def help_command(message: types.Message) -> None:
    """
    Help command bot
    """

    message_for_user: str = "".join(await text_for_help_command(username=message.from_user.username))

    await message.answer_animation(
        animation=FSInputFile("bot/static/help.gif"),
        caption=message_for_user,
        parse_mode=ParseMode.HTML
    )


@command_router.message(Command("clear"))
async def clear_command(message: types.Message, state: FSMContext) -> None:
    """
    Clear command bot
    """
    
    await state.clear()
    await message.reply(text="Очистка состояний прошла успешно")


@command_router.message(Command("profile"))
async def my_profile_command(message: types.Message) -> None:
    """
    Unique user profile
    """

    user_photo = dict(dict(await message.from_user.get_profile_photos()).get("photos")[0][0]).get("file_id")
    msg_for_user_profile = "".join(await text_for_profile(username=message.from_user.first_name))

    await message.answer_photo(
        photo=user_photo,
        caption=msg_for_user_profile,
        parse_mode=ParseMode.HTML,
        reply_markup=await btn_for_profile()
    )