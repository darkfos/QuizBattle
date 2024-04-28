from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def btn_for_profile() -> InlineKeyboardBuilder.as_markup:
    """
    Inline button for profile
    """

    kb_profile: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_profile.row(
        InlineKeyboardButton(
            text="📊 Мировая статистика", callback_data="stats_profbtn"
        )
    )

    kb_profile.row(
        InlineKeyboardButton(
            text="📌 Изменить моё фото", callback_data="change_photo_profbtn",
        ),
        InlineKeyboardButton(
            text="📍 Изменить моё имя", callback_data="change_username_profbtn"
        )
    )

    kb_profile.row(
        InlineKeyboardButton(
            text="📈 Моя история игр", callback_data="my_history_profbtn"
        ),
        InlineKeyboardButton(
            text="📝 Мои отзывы", callback_data="my_review_profbtn"
        )
    )

    kb_profile.row(
        InlineKeyboardButton(
            text="⛔ Удалить профиль",
            callback_data="delete_me_profbtn"
        )
    )

    return kb_profile.as_markup()