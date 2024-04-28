from typing import List

async def game_options() -> List[str]:
    """
    Return game version
    """

    game_versions: List[str] = [
        "👑 Мастер перевода",
        "📝 Скоростной букварь",
        "💡 Обратный перевод"
    ]

    return game_versions