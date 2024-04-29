from aiogram.fsm.state import State, StatesGroup


class ChangeUserName(StatesGroup):

    user_name: str = State()


class ChangeUserPhoto(StatesGroup):

    photo: str = State()