from aiogram.fsm.state import State, StatesGroup


class YoutubeStates(StatesGroup):
    GET_URL = State()
    GET_OPTIONS = State()
