from emoji import emojize
from typing import List
from datetime import datetime
from bot.req_api.user_api import UserApi
from bot.req_api.game_api import GameAPI

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


async def text_for_description() -> str:
    """
    Text for description bot
    """

    desc: str = "Я Quizy бот, который поможет тебе изучить новый язык путем интересных викторин!\n\nДавай начнем наше с тобой обучение!"
    return desc


async def text_for_help_command(username: str) -> List:
    """
    Return text for help command
    """

    msg_text: List= [
        "<b>Добро пожаловать в пункт поддержки {}</b>\n\n".format(username),
        "На данный момент имеются такие команды:\n\n",
        "⚙ /start - Запуск бота, начало работы с приложением\n",
        "⚙ /help - Пункт поддержки (сейчас мы здесь)\n",
        "⚙ /game - Главная команда для запуска и выбора режима игры\n",
        "⚙ /profile - Мой профиль, ваша личная страница\n",
        "⚙ /stats - Получить мировую статистику\n",
        "⚙ /review - Оставить свой отзыв\n",
        "⚙ /clear - Отменить какие-либо действия\n\n" + \
        "🏷 <b>Пояснение к видам игр:</b>\n\n",
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
        "🇳🇴 <b>Норвежский</b>"
    ]

    return msg_text

async def text_for_profile(username: str) -> List:
    """
    Return list text for profile command
    """

    #Get user info
    information_about_user: dict = await UserApi().get_full_user_info()

    #Get user rank
    rank = await GameAPI().get_rank_user()

    msg_text: List = [
        "Добро пожаловать в личный профиль {}!\n\n".format(username),
        "🕯 Ваша <b><i>личная</i></b> статистика:\n\n",
        f"🎭 Ваше имя: {information_about_user.get('name_user')}\n\n",
        f"🎯 Ваш счет: {information_about_user.get('score')}\n\n",
        f"🥇 Ваше место в рейтинге: {rank.get('user_rank') if isinstance(rank, dict) else rank}\n\n",
        f"🗓 Дата вашей регистрации: {(datetime.fromisoformat(information_about_user.get('date_create').replace('T', ' '))).date()}\n\n",
        f"📆 Дата обновления вашей информации: {(datetime.fromisoformat(information_about_user.get('date_update').replace('T', ' '))).date()}\n\n",
        f"📊 Ваше количество игр: {information_about_user.get('game_count')}\n\n",
        f"📊 Ваше общее количество игр: {len(information_about_user.get('histories'))}\n\n",
        f"📣 Ваше количество отзывов: {len(information_about_user.get('reviews'))}\n\n"
    ]

    return msg_text