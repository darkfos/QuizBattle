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
from bot.req_api.game_set import gts, gss
from bot.req_api.user_set import user_auth_set
from bot.req_api.history_api import HistoryApi, AddNewHistoryPDSchema


game = GameAPI()
message_router: Router = Router()
        


@message_router.callback_query(lambda message: message.data.endswith("gyp"))
async def choice_user_continue(clb: types.CallbackQuery, state: FSMContext) -> None:
    if "yes" in clb.data:
        game_r = await game.get_words()
        await clb.message.answer(f"Загаданное слово: <b>{gts.word}</b>", parse_mode=ParseMode.HTML)
        await state.set_state(GameTranslates.word_translate)
    else:
        await gss.procent_game_r()
        await clb.message.delete()
        await clb.message.answer(text="Игра окончена..")
        await HistoryApi().create_history(
            new_history=AddNewHistoryPDSchema(
                score=gss.score,
                right_word=gss.right_word,
                lose_word=gss.lose_word,
                procent_game=gss.procent_game,
                token=user_auth_set.token
            )
        )
        await state.clear()


@message_router.callback_query(lambda message: message.data.endswith("profbtn"))
async def chice_profile_btn(
    clb: types.CallbackQuery,
    state: FSMContext
) -> None:
    if clb.data == "my_history_profbtn":
        all_my_histories: list = await HistoryApi().get_my_histories()

        count_history = 0
        if all_my_histories:
            for history in all_my_histories:
                await clb.message.answer(
                    text=f"История <b>№{count_history}</b>\n\n👑 Счет: {history.get('score')}\n✅ Количество верных слов: {history.get('right_word')}\n❌ Количество неверных слов: {history.get('lose_word')}\n📝 Коэффицент правильности: {history.get('procent_game')}",
                    parse_mode=ParseMode.HTML
                )
                count_history += 1
        else:
            await clb.message.answer(
                text="У вас отсутствует история, нужно это исправить!"
            )

@message_router.callback_query(IsLanguageFilter())
async def language_sel(message: types.CallbackQuery, state: FSMContext) -> None:
    """
    Choice game mode
    """

    country_name: str = ""
    match message.data:
        case "game_spain_gmt":
            country_name = "es"
        case "game_england_gmt":
            country_name = "en"
        case "game_germany_gmt":
            country_name = "de"

    #Set country name
    game.code = country_name
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


    if game_mode_name == "translate":
        game_r = await game.get_words()
        game_state_translate = gm_t(
            secret_word=game_r.secret_word,
            translate_in_russo=game_r.translate_in_russo
        )

        await message.answer(f"Загаданное слово: <b>{game_state_translate.secret_word}</b>", parse_mode=ParseMode.HTML)
        await state.set_state(GameTranslates.word_translate)
    elif game_mode_name == "speed_translate":
        pass
    elif game_mode_name == "reverse_translate":
        pass

@message_router.message()
async def all_other_message(message: types.Message) -> None:
    """
    Proccessing other message from user
    """

    await message.answer(text="Не понимаю ваш запрос")