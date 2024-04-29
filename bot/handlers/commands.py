from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from bot.utils.text.command_text import (text_for_start_command,
                                        text_for_help_command,
                                        text_for_profile)

from bot.key.inln_kb import btn_for_profile, btn_for_game_country
from bot.states.CreateReview import CreateReview
from bot.states.GameState import Game
from bot.req_api.game_api import GameAPI
from bot.req_api.user_api import UserApi


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

    msg_for_user_profile = "".join(await text_for_profile(username=message.from_user.first_name))
    
    #Get user photo
    user_photo = dict(await UserApi().get_user_info()).get("photo")

    if user_photo is None:
        user_photo = dict(dict(await message.from_user.get_profile_photos()).get("photos")[0][0]).get("file_id")
    await message.answer_photo(
        photo=user_photo,
        caption=msg_for_user_profile,
        parse_mode=ParseMode.HTML,
        reply_markup=await btn_for_profile()
    )


@command_router.message(Command("review"))
async def create_review(message: types.Message, state: FSMContext):
    """
    Create review by user
    """

    await message.answer(text="Ваш запрос принят..\n<b>Пожалуйста введите сообщение для отзыва</b>", parse_mode=ParseMode.HTML)
    await state.set_state(CreateReview.message)


@command_router.message(Command("stats"))
async def stats_command(message: types.Message, state: FSMContext):
    """
    Get stats
    """

    all_stats_user: list = await GameAPI().get_stats()

    if all_stats_user:
        text_top_list: str = ""
        count_stats: int = 1
        for usr in all_stats_user[:7]:
            text_top_list += f"Место <b><i>#{count_stats}</i></b>\nПользователь: {usr.get('user_name')}\nКоличество очков: {usr.get('score')}\n\n"
            count_stats += 1

        await message.answer(text="🌍 Мировая статистика: \n\n"+text_top_list, parse_mode=ParseMode.HTML)
    else:
        await message.answer(text="К сожалению мировая статистика пока пуста...\nНо вы можете занять свой топ!")


@command_router.message(Command("game"))
async def game_options(message: types.Message, state: FSMContext):
    """
    Send all list game in bot
    """

    await message.answer(
        text="🏳 Пожалуйста выберите <b><i>язык</i></b> для игры: ",
        parse_mode=ParseMode.HTML,
        reply_markup=await btn_for_game_country()
    )
    
    await state.set_state(Game.language)