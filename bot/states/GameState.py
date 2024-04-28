from aiogram.fsm.state import State, StatesGroup


class Game(StatesGroup):

    language: str = StatesGroup()
    game_mode: str = StatesGroup()


class GameSpeed(StatesGroup):
    pass


class GameTranslate(StatesGroup):
    pass

class GameReverseTranslate(StatesGroup):
    pass