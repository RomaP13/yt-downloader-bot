from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.message_utils import edit_quality_message
from youtube_scripts.streams import get_video_streams


async def get_quality(call: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    streams = data.get("streams")
    only_video = data.get("option") == "video"
    video_streams_by_res = await get_video_streams(streams, only_video)
    await edit_quality_message(call, bot, state,
                               list(video_streams_by_res.keys()))
    await state.update_data(video_streams_by_res=video_streams_by_res)
