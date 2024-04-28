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
        "⚙ /clear - Отменить какие-либо действия"
    ]

    return msg_text

async def text_for_profile(username: str) -> List:
    """
    Return list text for profile command
    """

    msg_text: List = [
        "Добро пожаловать в личный профиль {}!\n\n".format(username),
        "🕯 Ваша <b><i>личная</i></b> статистика:\n\n",
        "🎭 Ваше имя: \n\n"
        "🎯 Ваш счет: \n\n",
        "🥇 Ваше место в рейтинге: \n\n",
        "🗓 Дата вашей регистрации: \n\n",
        "📆 Дата обновления вашей информации: \n\n",
        "📊 Ваше количество игр: \n\n",
        "📣 Ваше количество отзывов: \n\n"
    ]

    return msg_text