from aiogram import Router, types
from aiogram.enums.parse_mode import ParseMode
from bot.states.CreateReview import CreateReview
from aiogram.fsm.context import FSMContext
from bot.states.GameState import Game, GameTranslate as GameTranslates, GameSpeed, GameReverseTranslate
from api.backend.schemas.GamePDSchema import GameTranslate as gm_t
from bot.filters.IsLanguage import IsLanguageFilter, IsGameModeFilter
from bot.key.reply_kb import btn_for_game
from bot.key.inln_kb import generate_btn_for_game_translate
from bot.req_api.game_api import GameAPI
from bot.req_api.user_api import UserApi
from bot.req_api.game_set import gts


state_router: Router = Router()


@state_router.message(GameTranslates.word_translate)
async def translate_word(message: types.Message, state: FSMContext) -> None:
    """
    User translate word
    """

    await state.update_data(word_translate=message.text)
    if message.text.lower() == gts.translate_word.lower():


        #Update user score
        await UserApi().update_user_score(score=5)
        await message.answer(text="Отлично, ты получил 5 поинтов 🏆!")
        await message.answer(text=f"Поздравляю {message.from_user.first_name}, ты правильно перевёл слово!\n\nЖелаешь продолжить?",
                              reply_markup=await generate_btn_for_game_translate())

    else:
        await message.answer(text="К сожалению ваш перевод оказался неверным..\n\nЖелаете продолжить?",
                             reply_markup=await generate_btn_for_game_translate())
        

@state_router.message(CreateReview.message)
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