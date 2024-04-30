from aiogram import Router, types
from aiogram.enums.parse_mode import ParseMode
from bot.states.CreateReview import CreateReview
from aiogram.fsm.context import FSMContext
from bot.states.GameState import Game, GameTranslate as GameTranslates, GameSpeed, GameReverseTranslate
from api.backend.schemas.GamePDSchema import GameTranslate as gm_t
from bot.filters.IsLanguage import IsLanguageFilter, IsGameModeFilter
from bot.key.reply_kb import btn_for_game
from bot.key.inln_kb import generate_btn_for_game_translate, delete_profile_btn
from bot.filters.DeletePrifle import DeleteProfile
from bot.req_api.game_api import GameAPI
from bot.req_api.game_set import gts, gss
from bot.req_api.user_set import user_auth_set
from bot.req_api.user_api import UserApi
from bot.req_api.history_api import HistoryApi, AddNewHistoryPDSchema
from bot.req_api.review_api import ReviewAPI
from bot.states.UserProfileStates import ChangeUserName, ChangeUserPhoto
from random import randrange
from datetime import datetime


game = GameAPI()
message_router: Router = Router()


@message_router.callback_query(lambda message: message.data.endswith("ed"))
async def speed_game_continue(clb: types.CallbackQuery, state: FSMContext) -> None:
    if "yes" in clb.data:
        game_r = await game.get_words()
        game_state_translate = gm_t(
            secret_word=game_r.secret_word,
            translate_in_russo=game_r.translate_in_russo
        )

        await clb.message.answer(f"Загаданное слово: <b>{game_state_translate.secret_word}</b>\n\nВремя на перевод: <b>5</b> секунд", parse_mode=ParseMode.HTML)
        gss.game_time = datetime.now()
        await state.set_state(GameSpeed.word_translate)
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


@message_router.callback_query(lambda message: message.data.endswith("rt"))
async def choice_user_continue(clb: types.CallbackQuery, state: FSMContext) -> None:
    if "yes" in clb.data:
        game_r = await game.get_words()
        await clb.message.answer(f"Загаданное слово: <b>{gts.translate_word}</b>", parse_mode=ParseMode.HTML)
        await state.set_state(GameReverseTranslate.word_translate)
    else:
        await gss.procent_game_r()
        await clb.message.delete()
        await clb.message.answer(text="🛑 Игра окончена..")
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


@message_router.callback_query(lambda message: message.data.endswith("gyp"))
async def choice_user_continue(clb: types.CallbackQuery, state: FSMContext) -> None:
    if "yes" in clb.data:
        game_r = await game.get_words()
        await clb.message.answer(f"Загаданное слово: <b>{gts.word}</b>", parse_mode=ParseMode.HTML)
        await state.set_state(GameTranslates.word_translate)
    else:
        await gss.procent_game_r()
        await clb.message.delete()
        await clb.message.answer(text="🛑 Игра окончена..")
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
                # await clb.message.answer(
                #     text=f"История <b>№{count_history}</b>\n\n👑 Счет: {history.get('score')}\n✅ Количество верных слов: {history.get('right_word')}\n❌ Количество неверных слов: {history.get('lose_word')}\n📝 Коэффицент правильности: {history.get('procent_game')}",
                #     parse_mode=ParseMode.HTML
                # )
                count_history += 1
            await clb.message.answer(text=f"📚 Количество ваших историй игр: {count_history}")
        else:
            await clb.message.answer(
                text="У вас отсутствует история 📌, нужно это исправить!"
            )
    elif clb.data == "change_username_profbtn":
        await clb.answer("💡 Вы выбрали опцию изменить имя")
        await clb.message.answer("✏ Введите ваше <b>новое имя:</b> ", parse_mode=ParseMode.HTML)
        await state.set_state(ChangeUserName.user_name)   

    elif clb.data == "delete_me_profbtn":
        await clb.message.answer("Вы выбрали опцию <b>Удалить профиль</b> 🗑, вы уверены?",
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=await delete_profile_btn())
    
    elif clb.data == "stats_profbtn":
        await clb.answer("💡 Вы выбрали опцию мировая статистика")
        
        all_stats_user: list = await GameAPI().get_stats()

        if all_stats_user:
            text_top_list: str = ""
            count_stats: int = 1
            for usr in all_stats_user[:7]:
                text_top_list += f"Место <b><i>#{count_stats}</i></b>\nПользователь: {usr.get('user_name')}\nКоличество очков: {usr.get('score')}\n\n"
                count_stats += 1

            await clb.message.answer(text="📊 Мировая статистика: \n\n"+text_top_list, parse_mode=ParseMode.HTML)
        else:
            await clb.message.answer(text="К сожалению мировая статистика пока пуста...\nНо вы можете занять свой топ!")
    elif clb.data == "change_photo_profbtn":
        await clb.answer("💡 Вы выбрали опцию, обновить фото")
        await clb.message.answer("📷 Жду вашу новую фотографию..")
        await state.set_state(ChangeUserPhoto.photo)
    elif clb.data == "my_review_profbtn":

        all_review: list = dict(await UserApi().get_full_user_info()).get("reviews")
        await clb.message.answer(text=f"📚 Количество ваших отзывов: {len(all_review)}")


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
        case "game_franch_gmt":
            country_name = "fr"
        case "game_japanese_gmt":
            country_name = "ja"
        case "game_finnish_gmt":
            country_name = "fi"
        case "game_norway_gmt":
            country_name = "de"

    #Set country name
    game.code = country_name
    await state.update_data(language=country_name)
    await state.set_state(Game.game_mode)
    await message.message.answer(
        text=f"Отлично был выбран <b>{country_name}</b> язык 🏳, пожалуйста выберите режим игры...",
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

    await message.answer(text=f"<b>Отлично</b>, игра начинается ⏱ {message.from_user.first_name}", reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML)


    if game_mode_name == "translate":
        game_r = await game.get_words()
        game_state_translate = gm_t(
            secret_word=game_r.secret_word,
            translate_in_russo=game_r.translate_in_russo
        )

        await message.answer(f"📦 Загаданное слово: <b>{game_state_translate.secret_word}</b>", parse_mode=ParseMode.HTML)
        await state.set_state(GameTranslates.word_translate)
    elif game_mode_name == "speed_translate":
        game_r = await game.get_words()
        game_state_translate = gm_t(
            secret_word=game_r.secret_word,
            translate_in_russo=game_r.translate_in_russo
        )

        await message.answer(f"📦 Загаданное слово: <b>{game_state_translate.secret_word}</b>\n\nВремя на перевод: <b>5</b> секунд", parse_mode=ParseMode.HTML)
        gss.game_time = datetime.now()
        await state.set_state(GameSpeed.word_translate)

    elif game_mode_name == "reverse_translate":
        game_r = await game.get_words()
        game_state_translate = gm_t(
            secret_word=game_r.secret_word,
            translate_in_russo=game_r.translate_in_russo
        )

        await message.answer(f"📦 Слово: {game_r.translate_in_russo}, переведи его..")
        await state.set_state(GameReverseTranslate.word_translate)


@message_router.callback_query(DeleteProfile())
async def delete_profile_user(clb: types.CallbackQuery):
    """
        Delete profile
    """

    if clb.data == "yes_del":
        await clb.message.delete()
        req_del: bool = await UserApi().delete_profile()

        if req_del:
            await clb.answer(text="✅ Ваш профиль был удалён")
        else:
            await clb.answer(text="❌ Не удалось удалить профиль")
    else:
        await clb.message.delete()
        await clb.answer(text="❗ Отмена операции удаления профиля")


@message_router.message()
async def all_other_message(message: types.Message) -> None:
    """
    Proccessing other message from user
    """

    await message.answer(text="♾ Не понимаю ваш <i>запрос</i>", parse_mode=ParseMode.HTML)