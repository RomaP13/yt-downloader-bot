import logging

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.basic import get_audio
from handlers.media_handler import handle_download
from handlers.resolution import get_resolutions
from utils.message_utils import edit_message


LOADING_MESSAGE = """
The file is being prepared and will be sent soon. Please wait.
"""


async def select_content(call: CallbackQuery, bot: Bot,
                         state: FSMContext) -> None:
    await bot.answer_callback_query(call.id)

    assert call.data is not None, "'call.data' is None in select_resolution"
    assert call.message is not None, "'call.message' is None in select_resolution"

    option = call.data.split("_")[1]
    await state.update_data(option=option)

    if option in ["video", "both"]:
        await get_resolutions(call, bot, state)

    if option == "audio":
        await edit_message(bot, call.from_user.id,
                           call.message.message_id, LOADING_MESSAGE)
        await get_audio(state)
        await handle_download(call, bot, state)


async def select_resolution(call: CallbackQuery, bot: Bot,
                            state: FSMContext) -> None:
    await bot.answer_callback_query(call.id)

    assert call.data is not None, "'call.data' is None in select_resolution"
    assert call.message is not None, "'call.message is None in select_resolution"

    await edit_message(bot, call.from_user.id,
                       call.message.message_id, LOADING_MESSAGE)

    res = call.data.split("_")[1]
    data = await state.get_data()
    video_streams_by_res = data.get("video_streams_by_res")
    option = data.get("option")

    if video_streams_by_res is not None:
        v_stream = video_streams_by_res.get(res)
        await state.update_data(v_stream=v_stream)

        if option == "both" and v_stream.is_adaptive:
            await get_audio(state)
    else:
        logging.warning("Couldn't find 'video_streams_by_res'")

    await handle_download(call, bot, state)
