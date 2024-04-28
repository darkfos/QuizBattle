from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from bot.utils.text.command_text import text_for_start_command


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