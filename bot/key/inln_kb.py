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


async def btn_for_game_country() -> InlineKeyboardBuilder.as_markup:
    """
    Return btn builder for game
    """

    btn_game_country: InlineKeyboardBuilder = InlineKeyboardBuilder()

    btn_game_country.row(
        InlineKeyboardButton(
            text="🇬🇧 Английский (Британский)", callback_data="game_england_gmt"
        ),
        InlineKeyboardButton(
            text="🇪🇸 Испанский", callback_data="game_spain_gmt"
        )
    )

    btn_game_country.row(
        InlineKeyboardButton(
            text="🇪🇸 Испанский", callback_data="game_spain_gmt"
        ),
        InlineKeyboardButton(
            text="🇩🇪 Немецкий", callback_data="game_germany_gmt"
        )
    )

    btn_game_country.row(
        InlineKeyboardButton(
            text="🇫🇷 Французский", callback_data="game_franch_gmt"
        ),
        InlineKeyboardButton(
            text="🇯🇵 Японский", callback_data="game_japanese_gmt"
        )
    )


    btn_game_country.row(
        InlineKeyboardButton(
            text="🇫🇮 Финский", callback_data="game_finnish_gmt"
        ),
        InlineKeyboardButton(
            text="🇳🇴 Норвежский", callback_data="game_norway_gmt"
        )
    )


    return btn_game_country.as_markup()


async def generate_btn_for_game_translate() -> InlineKeyboardBuilder.as_markup:

    btn_game_y_n: InlineKeyboardBuilder = InlineKeyboardBuilder()

    btn_game_y_n.add(
        InlineKeyboardButton(
            text="Да", callback_data="yes_gyp"
        ),
        InlineKeyboardButton(
            text="Нет", callback_data="no_gyp"
        )
    )

    return btn_game_y_n.as_markup()


async def generate_btn_for_game_reverse_translate() -> InlineKeyboardBuilder.as_markup:

    btn_game_y_n: InlineKeyboardBuilder = InlineKeyboardBuilder()

    btn_game_y_n.add(
        InlineKeyboardButton(
            text="Да", callback_data="yes_rt"
        ),
        InlineKeyboardButton(
            text="Нет", callback_data="no_rt"
        )
    )

    return btn_game_y_n.as_markup()


async def generate_btn_for_game_speed_translate() -> InlineKeyboardBuilder.as_markup:

    btn_game_y_n: InlineKeyboardBuilder = InlineKeyboardBuilder()

    btn_game_y_n.add(
        InlineKeyboardButton(
            text="Да", callback_data="yes_speed"
        ),
        InlineKeyboardButton(
            text="Нет", callback_data="no_speed"
        )
    )

    return btn_game_y_n.as_markup()


async def delete_profile_btn() -> InlineKeyboardBuilder.as_markup:

    btn_for_delete_profile: InlineKeyboardBuilder = InlineKeyboardBuilder()


    btn_for_delete_profile.add(
        InlineKeyboardButton(
            text="Да", callback_data="yes_del"
        ),
        InlineKeyboardButton(
            text="Нет", callback_data="no_del"
        )
    )

    return btn_for_delete_profile.as_markup()