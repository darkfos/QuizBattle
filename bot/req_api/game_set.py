from datetime import datetime

class GameTranslateSettings:

    def __init__(self) -> None:
        self.word: str = ""
        self.translate_word: str = ""


class GameStateSett:

    def __init__(self) -> None:
        self.score: int = 0
        self.right_word: int = 0
        self.lose_word: int = 0
        self.procent_game: int = 0
        self.game_time: datetime

    async def procent_game_r(self):
        try:
            self.procent_game: int = self.right_word / self.lose_word
        except Exception as ex:
            self.procent_game: int = 0

gts = GameTranslateSettings()
gss = GameStateSett()