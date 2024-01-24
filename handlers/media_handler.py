import logging
import pathlib
from typing import Dict

from aiogram import Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from media_processing.combine_audio_video import combine
from utils.statesyoutube import YoutubeStates
from youtube_scripts.media_downloader import download_file


def get_file_paths(title: str) -> Dict[str, str]:
    return {
        "audio": f"media/audio/{title}.mp4",
        "video": f"media/video/{title}.mp4",
        "combined": f"media/combined/{title}.mp4"
    }


async def send_video(call: CallbackQuery, file_path: str) -> None:
    assert call.message is not None, "'call.message' is None in 'send_video'"

    file = FSInputFile(file_path)

    await call.message.answer_video(file)

    logging.info("Video sent successfully: %s", file_path)


async def send_audio(call: CallbackQuery, file_path: str) -> None:
    assert call.message is not None, "'call.message' is None in 'send_audio'"

    file = FSInputFile(file_path)
    await call.message.answer_audio(file)

    logging.info("Audio sent successfully: %s", file_path)


# Function to combine video with audio and send it
async def process_and_send_video(call: CallbackQuery, state: FSMContext,
                                 paths: Dict[str, str]) -> None:
    combine(paths)
    await send_video(call, paths["combined"])


# Function to clear state and delete files
async def clear_state_and_files(state: FSMContext,
                                paths: Dict[str, str]) -> None:
    await state.clear()

    for path in paths.values():
        p = pathlib.Path(path)
        try:
            p.unlink()
        except FileNotFoundError:
            pass


async def handle_download(call: CallbackQuery, bot: Bot,
                          state: FSMContext) -> None:
    data = await state.get_data()

    v_stream = data.get("v_stream")
    a_stream = data.get("a_stream")
    title = data.get("title")

    assert title is not None, "'title' is None"
    paths = get_file_paths(title)

    video_downloaded = download_file(paths["video"], v_stream) if v_stream else False
    audio_downloaded = download_file(paths["audio"], a_stream) if a_stream else False

    if video_downloaded and audio_downloaded:
        await process_and_send_video(call, state, paths)
    elif audio_downloaded:
        await send_audio(call, paths["audio"])
    elif video_downloaded:
        await send_video(call, paths["video"])
    else:
        error_message = "Error: Unable to download the file. " \
                        "The file size may have exceeded the limit. " \
                        "Please try again or choose a lower resolution."

        assert call.message is not None, "'message' is None in handle_download"
        await call.message.answer(error_message)
        logging.warning("No video or audio stream downloaded.")

    await clear_state_and_files(state, paths)
    await state.set_state(YoutubeStates.GET_URL)
