from aiogram import Bot
from aiogram.types import Message, CallbackQuery, Union
from aiogram.fsm.context import FSMContext

from handlers.error_handler import get_error
from keyboards.inline import (
    get_main_inline_keyboard,
    get_confirm_download_inline_keyboard,
)
from utils.message_utils import edit_message
from utils.statesyoutube import YoutubeStates
from youtube_scripts.streams import get_streams, get_audio_stream
from youtube_scripts.title import get_title


async def get_start(message: Message, state: FSMContext) -> None:
    await state.set_state(YoutubeStates.GET_URL)
    await message.answer(
        "Hello! The bot was started. For working, send me a link from YouTube."
    )


async def get_youtube_url(
    event: Union[Message, CallbackQuery], bot: Bot, state: FSMContext
) -> None:
    await state.set_state(YoutubeStates.GET_OPTIONS)

    keyboard = get_main_inline_keyboard()
    if isinstance(event, Message):
        sent_message = await event.answer("Choose format:", reply_markup=keyboard)
        await state.update_data(bot_message=sent_message)
    else:
        await edit_message(
            bot,
            event.from_user.id,
            event.message.message_id,
            "Choose format:",
            keyboard,
        )

    data = await state.get_data()
    url = data.get("next_url")
    if url is None and isinstance(event, Message):
        url = event.text
        assert url is not None, "'url' is None"

    # If the URL is not set and the event is a CallbackQuery,
    # notify the user of an error and finish the function
    if url is None and isinstance(event, CallbackQuery):
        await get_error(bot, event, state)
        return

    streams = get_streams(url)
    title = get_title(url)

    await state.update_data(streams=streams)
    await state.update_data(title=title)


async def get_next_youtube_url(
    message: Message, bot: Bot, state: FSMContext
) -> None:
    keyboard = get_confirm_download_inline_keyboard()
    url = message.text
    assert url is not None, "'url' is None in get_next_youtube_url"
    next_title = get_title(url)

    text = f"You sent the second url. \
    Do you want to download this audio/video: {next_title}?"
    await message.answer(
        text=text,
        reply_markup=keyboard,
    )
    await state.update_data(next_url=url)


async def get_audio(state: FSMContext) -> None:
    data = await state.get_data()
    streams = data.get("streams")
    a_stream = get_audio_stream(streams)
    await state.update_data(a_stream=a_stream)
