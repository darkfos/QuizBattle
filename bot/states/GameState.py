from aiogram.fsm.state import State, StatesGroup


class Game(StatesGroup):

    language: str = State()
    game_mode: str = State()


class GameSpeed(StatesGroup):
    pass


class GameTranslate(StatesGroup):
    
    word_translate: str = State()
    continue_or_break: bool = State()

class GameReverseTranslate(StatesGroup):
    pass