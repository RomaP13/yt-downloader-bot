from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import (
    get_main_inline_keyboard,
    get_confirm_download_inline_keyboard,
)
from utils.statesyoutube import YoutubeStates
from youtube_scripts.streams import get_streams, get_audio_stream
from youtube_scripts.title import get_title


async def get_start(message: Message, state: FSMContext) -> None:
    await state.set_state(YoutubeStates.GET_URL)
    await message.answer(
        "Hello! The bot was started. For working, send me a link from YouTube."
    )


async def get_youtube_url(message: Message, bot: Bot,
                          state: FSMContext) -> None:
    await state.set_state(YoutubeStates.GET_OPTIONS)

    keyboard = get_main_inline_keyboard()
    sent_message = await message.answer("Choose format:", reply_markup=keyboard)

    url = message.text
    assert url is not None, "'url' is None"
    streams = get_streams(url)
    title = get_title(url)

    await state.update_data(streams=streams)
    await state.update_data(title=title)
    await state.update_data(bot_message=sent_message)


async def get_another_youtube_url(
    message: Message, bot: Bot, state: FSMContext
) -> None:
    keyboard = get_confirm_download_inline_keyboard()
    url = message.text
    assert url is not None, "'url' is None in get_another_youtube_url"
    another_title = get_title(url)

    text = f"You sent the second url. Do you want to download this audio/video: {another_title}?"
    await message.answer(
        text=text,
        reply_markup=keyboard,
    )


async def get_audio(state: FSMContext) -> None:
    data = await state.get_data()
    streams = data.get("streams")
    a_stream = get_audio_stream(streams)
    await state.update_data(a_stream=a_stream)
