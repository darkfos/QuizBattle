from aiogram.fsm.state import State, StatesGroup


class CreateReview(StatesGroup):

    message: str = State()