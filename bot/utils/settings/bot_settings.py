from aiogram.methods.set_my_description import SetMyDescription
from aiogram.methods.set_my_commands import SetMyCommands
from aiogram.methods.set_my_name import SetMyName
from bot.utils.text.command_text import text_for_description
from aiogram.types import BotCommand

from aiogram import Bot


async def set_commands_for_bot(bot: Bot) -> None:
    """
        Set commands for bot
    """

    return await bot(SetMyCommands(
        commands=[
                BotCommand(command="game", description="Режим игры"),
                BotCommand(command="start", description="Начало работы"),
                BotCommand(command="help", description="Поддержка"),
                BotCommand(command="profile", description="Мой профиль"),
                BotCommand(command="stats", description="Мировая статистика"),
                BotCommand(command="review", description="Оставить отзыв"),
                BotCommand(command="clear", description="Очистить память"),
                BotCommand(command="country_information", description="Информация о стране")
        ]
    ))


async def set_my_description_for_bot(bot: Bot) -> None:
    """
        Set description for bot
    """

    return await bot(SetMyDescription(
        description=await text_for_description()
    ))