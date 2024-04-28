from emoji import emojize
from typing import List


async def text_for_start_command(username: str) -> List:
    """
    Return text for start command
    """

    msg_text: List = [
        f"Привет, <b>{username}</b>, я бот для изучения иностранных языков!\n\n",
        "Здесь ты сможешь подтянуть свои знания, путем обычной игры..\n",
        "<b><i>На выбор есть несколько языков для изучения:</i></b>\n\n",
        f"🇬🇧 English <b>-</b> Английский\n🇪🇸 Spain <b>-</b> Испанский\n🇩🇪 Germany <b>-</b> Немецкий\n\n",
        "Давай же не затягивай, поскорее начнем изучение!"
    ]

    return msg_text