from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from bot.utils.settings.game_options import game_options


async def btn_for_game() -> ReplyKeyboardBuilder:
    """
    Button for game
    """

    btn_game = ReplyKeyboardBuilder()

    vr_gm: list = await game_options()

    for game_ver in vr_gm:
        btn_game.add(
            KeyboardButton(text=game_ver)
        )

    return btn_game