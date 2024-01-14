from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_main_inline_keyboard, get_confirm_download_inline_keyboard
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
    await message.answer("Choose format:", reply_markup=keyboard)

    url = message.text
    streams = await get_streams(url)
    title = await get_title(url)

    await state.update_data(streams=streams)
    await state.update_data(title=title)
    await state.update_data(message=message)


async def get_another_youtube_url(message: Message, bot: Bot,
                                  state: FSMContext) -> None:
    print("ANOTHER URL")

    # Check if the current state is GET_OPTIONS
    current_state = await state.get_state()
    if current_state is not None and current_state != YoutubeStates.GET_OPTIONS:
        return

    # Set the state to GET_OPTIONS if it's not set already
    if current_state is None:
        await state.set_state(YoutubeStates.GET_OPTIONS)
    keyboard = get_confirm_download_inline_keyboard()
    await message.answer("You sent the second url. Do you want to download this audio/video: title?", reply_markup=keyboard)


async def get_audio(message: Message, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    streams = data.get("streams")
    a_stream = await get_audio_stream(streams)
    await state.update_data(a_stream=a_stream)
