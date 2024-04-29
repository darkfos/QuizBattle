from aiogram.fsm.state import State, StatesGroup
from datetime import datetime


class Game(StatesGroup):

    language: str = State()
    game_mode: str = State()


class GameSpeed(StatesGroup):
    
    word_translate: str = State()
    continue_or_break: bool = State()
    time_now: datetime


class GameTranslate(StatesGroup):
    
    word_translate: str = State()
    continue_or_break: bool = State()


class GameReverseTranslate(StatesGroup):
    
    word_translate: str = State()
    continue_or_break: bool = State()
