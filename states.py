from aiogram.fsm.state import StatesGroup, State


class ToolsState(StatesGroup):

    qr = State()

    link = State()

    text = State()