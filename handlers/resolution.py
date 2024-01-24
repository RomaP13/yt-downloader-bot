from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_resolution_inline_keyboard
from utils.message_utils import edit_message
from youtube_scripts.streams import get_video_streams


async def get_resolutions(call: CallbackQuery, bot: Bot,
                          state: FSMContext) -> None:
    assert call.message is not None, "'call.message' is None in get_resolutions"

    data = await state.get_data()
    streams = data.get("streams")
    only_video = data.get("option") == "video"
    video_streams_by_res = get_video_streams(streams, only_video)

    keyboard = get_resolution_inline_keyboard(list(video_streams_by_res.keys()))

    await edit_message(bot, call.from_user.id,
                       call.message.message_id, "Choose a video resolution:", keyboard)
    await state.update_data(video_streams_by_res=video_streams_by_res)
