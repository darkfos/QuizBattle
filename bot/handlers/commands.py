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

    await message.answer(
        text="".join(("🏷 <b>Пояснение к видам игр:</b>\n\n",
        "💡<i>Мастер перевода</i> - Перевод слова с выбранного языка на русский, время неограниченно, количество получаемых очков при правильном ответе - <b>5</b>\n\n",
        "💡<i>Скоростной букварь</i> - Перевода слова с выбранного языка на русский на скорость, время - <b>3 секунжы</b>, количество получаемы очков при правильном ответе - <b>15</b>\n\n",
        "💡<i>Обратный перевод</i> - Перевода слова с русского на выбранный язык, время неограниченно, количество получаемых очков при правильном ответе - <b>5</b>\n\n",
        "\n\n🏳 <b>Доступные языки для игр:</b>\n\n",
        "🇬🇧 <b>Английский (Британский)</b>\n",
        "🇪🇸 <b>Испанский</b>\n",
        "🇩🇪 <b>Немецкий</b>\n",
        "🇫🇷 <b>Французский</b>\n",
        "🇯🇵 <b>Японский</b>\n",
        "🇫🇮 <b>Финский</b>\n",
        "🇳🇴 <b>Норвежский</b>")),
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


@command_router.message(Command("country_information"))
async def country_information(message: types.Message):
    """
    Send basic information about country
    """

    await message.answer_animation(animation=FSInputFile("bot/static/country.gif"),
        caption="Краткая информация об каждой стране...")
    

    dct_country: dict = {
        0: "🇬🇧 Великобритании",
        1: "🇪🇸 Испании",
        2: "🇩🇪 Германии",
        3: "🇫🇷 Франции",
        4: "🇯🇵 Японии",
        5: "🇫🇮 Финляндии",
        6: "🇳🇴 Норвегии"
    }

    dct_country_info: dict = {
        0: "Великобрита́ния (англ. Great Britain); официальное название — Соединённое Короле́вство Великобрита́нии и Се́верной Ирла́ндии (по–английски обычно сокращается до «United Kingdom») — «Соединённое Королевство») — островное государство на северо–западе Европы. Оно состоит из четырёх «исторических провинций» (по–английски — «countries», то есть «страны»): Англия, Шотландия, Уэльс и Северная Ирландия. Государство располагается на Британских островах.",
        1: "Испания – одна из самых колоритных и интересных стран Европы, имеющая богатейшую историю и привлекающая каждый год десятки миллионов туристов. Легенда гласит, что ее название произошло от финикийского слова «шпан», или «спан», что в переводе означает «кролик». Дело в том, что когда финикийцы впервые попали на испанский берег, их поразило количество этих зверьков, которыми буквально кишели все кусты.",
        2: "Германия удивляет многообразием и красотой природы: на Северном и Балтийском морях простираются гряды островов с песчаными пляжами и дюнами, а вдоль побережья – вересковые пустоши и болота. Густые смешанные леса и средневековые замки украшают долины рек, текущих среди холмов, которые так любили немецкие поэты-романтики. А на юге, отражаясь в чистых горных озёрах, возвышаются вершины Альп, самая высокая из которых –  Цугшпитце (ок. 3000 метров над уровнем моря).",
        3: "Фра́нция (фр. France) официальное название Францу́зская Респу́блика (фр. République française) – государство в Западной Европе, включающее в свой состав помимо материковой части ещё остров Корсика. Также в состав Франции входят: Гваделупа, Мартиника, Гвиана, Реюньон, Сен–Пьер и Микелон и о–ва Новая Каледония, Французская Полинезия и др. Общая площадь Франции составляет 551 000 кв. км, это самая крупная по территории страна в Западной Европе.",
        4: "Япония - страна восходящего солнца, загадочная земля на восточной окраине мира. Здесь все необычно: климат, жаркий на юге, где растут пальмы, очень холодный на севере, где четыре месяца в году лежит снег; а история этой страны, больше похожая на таинственную легенду, чем на реальность. Всех радует Япония удивительной красотой природы, атмосферой покоя, а также обилием развлечений - многих из которых нет ни в одной другой стране мира.",
        5: "Финляндия - государство на севере Европы в восточной части Скандинавского полуострова. Граничит с Швецией на западе, Норвегией на севере и Россией на востоке. Финляндия - это современное государство с высоким уровнем жизни, удобными маленькими городками и поселками, которое до сих пор имеет большие нетронутые природные ландшафты. Является парламентской республикой, в которой официальными языками признаны финский и шведский. ",
        6: "Норвегия, как и большинство стран Скандинавии, - королевство. Она занимает западную часть полуострова, но это не единственная ее территория. Ей также принадлежат архипелаг Шпицберген, несколько островов в Северном Ледовитом океане и одна заморская территория - остров Буве в Атлантике."
    }

    dct_country_url: dict = {
        0: "https://www.panda-travel.by/countries/velikobritaniya",
        1: "https://www.abcspain.ru/ob-ispanii/?utm_referrer=https%3A%2F%2Fwww.google.com%2F",
        2: "https://www.daad.ru/ru/ucheba-i-nauka-v-germanii/znakomstvo-s-germaniej/korotko-o-germanii/",
        3: "https://www.panda-travel.by/countries/frantsiya",
        4: "https://www.turkompot.ru/content/view/178/198/",
        5: "https://traveller-eu.ru/finland",
        6: "https://znaki.fm/places/norway/"
    }


    for i in range(7):
        message_txt_about_country = f"Краткий перечень об {dct_country.get(i)}:\n\n{dct_country_info.get(i)}\n\n<a href='{dct_country_url.get(i)}'>Подробнее</a>"
        await message.answer(
            text=message_txt_about_country,
            parse_mode=ParseMode.HTML
        )   