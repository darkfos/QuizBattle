from aiogram import Router, types
from aiogram.enums.parse_mode import ParseMode
from bot.states.CreateReview import CreateReview
from aiogram.fsm.context import FSMContext
from bot.states.GameState import Game, GameTranslate as GameTranslates, GameSpeed, GameReverseTranslate
from api.backend.schemas.GamePDSchema import GameTranslate as gm_t
from bot.filters.IsLanguage import IsLanguageFilter, IsGameModeFilter
from bot.key.reply_kb import btn_for_game
from bot.key.inln_kb import generate_btn_for_game_translate, generate_btn_for_game_reverse_translate, generate_btn_for_game_speed_translate
from bot.req_api.game_api import GameAPI
from bot.req_api.game_set import gss
from bot.req_api.user_api import UserApi, UpdateUserInfoPDSchema, UpdateUserPhotoPDSchema
from bot.req_api.game_set import gts
from bot.req_api.review_api import ReviewAPI, AddNewReviewPDSchema, user_auth_set
from bot.states.UserProfileStates import ChangeUserName, ChangeUserPhoto
from datetime import datetime


state_router: Router = Router()


@state_router.message(GameSpeed.word_translate)
async def translate_speed_word(message: types.Message, state: FSMContext) -> None:
    """
    Speed translate word
    """

    await state.update_data(word_translate=message.text)
    await UserApi().update_user_game_count(game_count=1)
    

    if message.text.lower() == gts.translate_word.lower():
        
        time_now = datetime.now()
        time_quest = (gss.game_time - time_now).total_seconds()

        if abs(int(time_quest)) <= 5:
            #Update user score
            await UserApi().update_user_score(score=15)
            gss.right_word = gss.right_word + 1
            gss.score = gss.score + 15
            await message.answer(text="Отлично, ты получил 15 поинтов 🏆!")
            await message.answer(text=f"📣 Поздравляю {message.from_user.first_name}, ты правильно перевёл слово!\n\nЖелаешь продолжить?",
                                reply_markup=await generate_btn_for_game_speed_translate())
        else:
            gss.lose_word = gss.lose_word + 1
            await message.answer(text="🔥 К сожалению вы не успели перевести на скорость слово, желаете повторить?",
                             reply_markup=await generate_btn_for_game_speed_translate())

    else:
        gss.lose_word = gss.lose_word + 1
        await message.answer(text="🔥 К сожалению ваш перевод оказался неверным..\n\nЖелаете продолжить?",
                             reply_markup=await generate_btn_for_game_speed_translate())
        


@state_router.message(GameTranslates.word_translate)
async def translate_word(message: types.Message, state: FSMContext) -> None:
    """
    User translate word
    """

    await state.update_data(word_translate=message.text)
    await UserApi().update_user_game_count(game_count=1)
    

    if message.text.lower() == gts.translate_word.lower():


        #Update user score
        await UserApi().update_user_score(score=5)
        gss.right_word = gss.right_word + 1
        gss.score = gss.score + 5
        await message.answer(text="Отлично, ты получил 5 поинтов 🏆!")
        await message.answer(text=f"📣 Поздравляю {message.from_user.first_name}, ты правильно перевёл слово!\n\nЖелаешь продолжить?",
                              reply_markup=await generate_btn_for_game_translate())

    else:
        gss.lose_word = gss.lose_word + 1
        await message.answer(text="🔥 К сожалению ваш перевод оказался неверным..\n\nЖелаете продолжить?",
                             reply_markup=await generate_btn_for_game_translate())


@state_router.message(GameReverseTranslate.word_translate)
async def translate_word(message: types.Message, state: FSMContext) -> None:
    """
    User translate word
    """

    await state.update_data(word_translate=message.text)
    await UserApi().update_user_game_count(game_count=1)
    

    if message.text.lower() == gts.word:


        #Update user score
        await UserApi().update_user_score(score=5)
        gss.right_word = gss.right_word + 1
        gss.score = gss.score + 5
        await message.answer(text="Отлично, ты получил 5 поинтов 🏆!")
        await message.answer(text=f"📣 Поздравляю {message.from_user.first_name}, ты правильно перевёл слово!\n\nЖелаешь продолжить?",
                              reply_markup=await generate_btn_for_game_reverse_translate())

    else:
        gss.lose_word = gss.lose_word + 1
        await message.answer(text="🔥 К сожалению ваш перевод оказался неверным..\n\nЖелаете продолжить?",
                             reply_markup=await generate_btn_for_game_reverse_translate())

@state_router.message(CreateReview.message)
async def get_message_review_from_user(
    message_from_user: types.Message,
    state: FSMContext
) -> None:
    """
    Create review
    """

    if message_from_user.content_type == "text":
        #Save review
        save_req = await ReviewAPI().create_review(
            new_review=AddNewReviewPDSchema(
                message=str(message_from_user.text),
                token=str(user_auth_set.token)
            )
        )

        if save_req:
            await state.update_data(message=message_from_user.text)
            await message_from_user.answer(text="✅ Отлично, ваш отзыв был сохранён!")
            await state.clear()
        else:
            await message_from_user.answer(text="❌ Не удалось сохранить ваш отзыв")
            await state.clear()
    else:
        await message_from_user.answer(text="❗ Ожидается текст!")
        await state.set_state(CreateReview.message)


@state_router.message(ChangeUserName.user_name)
async def change_user_name(
    message: types.Message,
    state: FSMContext
) -> None:
    """
    Change user name
    """

    if message.content_type == "text":
        new_user_name: str = message.text

        new_user_name = new_user_name.replace("<", "")
        new_user_name = new_user_name.replace(">", "")
        new_user_name = new_user_name.replace("/", "")
        new_user_name = new_user_name.replace("\\", "")

        
        req = await UserApi().update_user_name(
            data_update=UpdateUserInfoPDSchema(
                token=user_auth_set.token,
                name_user=new_user_name,
                date_update=datetime.now().date()
            )
        )

        if req:
            await message.answer(text="✅ Ваше имя было <b>успешно</b> изменено", parse_mode=ParseMode.HTML)
            await state.clear()
        else:
            await message.answer(text="❌ <b>Не удалось</b> обновить ваше имя", parse_mode=ParseMode.HTML)
            await state.clear()
    else:
        await message.answer(text="❗ Имя должно быть текстом!")
        await state.set_state(ChangeUserName.user_name)
    

@state_router.message(ChangeUserPhoto.photo)
async def change_user_photo(
    message: types.Message,
    state: FSMContext
) -> None:
    """
    Update user photo
    """
    
    if message.content_type == "photo":
        print(dict(message.photo[0]).get("file_id"))

        user_data_for_update: UpdateUserPhotoPDSchema = UpdateUserPhotoPDSchema(
            token=user_auth_set.token,
            photo=dict(message.photo[0]).get("file_id")
        )

        req_status_code: bool = await UserApi().update_user_photo(data_update=user_data_for_update)
        
        if req_status_code:
            await message.answer(text="✅ Ваша фотография была <b>успешно</b> обновлена", parse_mode=ParseMode.HTML)
        else:
            await message.answer(text="❌ Не удалось обновить вашу фотографию", parse_mode=ParseMode.HTML)

        await state.clear()
    else:
        await message.answer(text="❌ Не удалось обновить вашу фотограцию", parse_mode=ParseMode.HTML)
        await state.set_state(ChangeUserPhoto.photo)