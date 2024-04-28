from aiogram import Router, types
from aiogram.enums.parse_mode import ParseMode
from bot.states.CreateReview import CreateReview
from aiogram.fsm.context import FSMContext
from bot.states.GameState import Game
from bot.filters.IsLanguage import IsLanguageFilter, IsGameModeFilter
from bot.key.reply_kb import btn_for_game


message_router: Router = Router()


@message_router.message(CreateReview.message)
async def get_message_review_from_user(
    message: types.Message,
    state: FSMContext
) -> None:
    """
    Create review
    """

    if message.content_type == "text":
        await state.update_data(message=message.text)
        await message.answer(text="Отлично, ваш отзыв был сохранён!")
        await state.clear()
    else:
        await message.answer(text="Ожидается текст!")
        await state.set_state(CreateReview.message)


@message_router.callback_query(IsLanguageFilter())
async def language_sel(message: types.CallbackQuery, state: FSMContext) -> None:
    """
    Choice game mode
    """

    country_name: str = ""
    match message.data:
        case "game_spain_gmt":
            country_name = "Испанский"
        case "game_england_gmt":
            country_name = "Английский"
        case "game_germany_gmt":
            country_name = "Немецкий"

    await state.update_data(language=country_name)
    await state.set_state(Game.game_mode)
    await message.message.answer(
        text=f"Отлично был выбран <b>{country_name}</b> язык, пожалуйста выберите режим игры...",
        parse_mode=ParseMode.HTML,
        reply_markup=(await btn_for_game()).as_markup()
        )


@message_router.message(IsGameModeFilter())
async def game_mode(message: types.Message, state: FSMContext) -> None:
    """
    Choice game mode
    """

    game_mode_name: str = ""

    match message.text:
        case "👑 Мастер перевода":
            game_mode_name = "translate"
        case "📝 Скоростной букварь":
            game_mode_name = "speed_translate"
        case "💡 Обратный перевод":
            game_mode_name = "reverse_translate"

    await message.answer(text=f"Отлично, игра начинается {message.from_user.first_name}", reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(game_mode=game_mode_name)
    await state.clear()
    
    

@message_router.message()
async def all_other_message(message: types.Message) -> None:
    """
    Proccessing other message from user
    """

    await message.answer(text="Не понимаю ваш запрос")