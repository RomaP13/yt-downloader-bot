from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.message_utils import edit_message
from utils.statesyoutube import YoutubeStates


async def get_error(bot: Bot, call: CallbackQuery, state: FSMContext) -> None:
    assert call.message is not None, "'call.message' is None in get_error"
    await edit_message(
        bot,
        call.from_user.id,
        call.message.message_id,
        "Something went wrong. Please, try again.",
    )

    await state.clear()
    await state.set_state(YoutubeStates.GET_URL)
