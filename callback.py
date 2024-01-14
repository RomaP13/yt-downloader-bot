from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.message_utils import edit_loading_message
from handlers.quality import get_quality
from handlers.basic import get_audio
from handlers.download import handle_download

LOADING_MESSAGE = """
The file is being prepared and will be sent soon. Please wait.
"""


async def select_content(call: CallbackQuery, bot: Bot,
                         state: FSMContext) -> None:
    await bot.answer_callback_query(call.id)

    if call.data is None:
        return

    option = call.data.split("_")[1]
    await state.update_data(option=option)

    if option in ["video", "both"]:
        # await state.set_state(YoutubeStates.GET_QUALITY)
        await get_quality(call, bot, state)

    if option == "audio":
        await edit_loading_message(call, bot, LOADING_MESSAGE)
        await get_audio(call, bot, state)
        await handle_download(call, bot, state)

    # if option == "both":
        # await state.set_state(YoutubeStates.GET_AUDIO)
        # await state.set_state(YoutubeStates.DOWNLOADING_MEDIA)
        # await get_audio(call, bot, state)


async def select_quality(call: CallbackQuery, bot: Bot,
                         state: FSMContext) -> None:
    await bot.answer_callback_query(call.id)
    await edit_loading_message(call, bot, LOADING_MESSAGE)

    if call.data is None:
        return

    res = call.data.split("_")[1]
    data = await state.get_data()
    video_streams_by_res = data.get("video_streams_by_res")
    option = data.get("option")

    if video_streams_by_res is not None:
        v_stream = video_streams_by_res.get(res)
        await state.update_data(v_stream=v_stream)

        if option == "both" and v_stream.is_adaptive:
            await get_audio(call, bot, state)

    # await state.set_state(YoutubeStates.DOWNLOADING_MEDIA)

    await handle_download(call, bot, state)
