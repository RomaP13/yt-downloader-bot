from pathlib import Path
from typing import Dict

from aiogram import Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from media_processing.test import combine
from utils.statesyoutube import YoutubeStates
from youtube_scripts.download import download_files


def get_file_paths(title: str) -> Dict[str, str]:
    return {
        "audio": f"media/audio/{title}.mp4",
        "video": f"media/video/{title}.mp4",
        "combined": f"media/combined/{title}.mp4"
    }


async def send_video(call: CallbackQuery, file_path: str) -> None:
    file = FSInputFile(file_path)
    await call.message.answer_video(file)


async def send_audio(call: CallbackQuery, file_path: str):
    file = FSInputFile(file_path)
    await call.message.answer_audio(file)


async def process_and_send_video(call: CallbackQuery, state: FSMContext,
                                 paths: Dict[str, str]) -> None:
    await combine(paths)

    await send_video(call, paths["combined"])


async def clear_state_and_files(state: FSMContext,
                                paths: Dict[str, str]) -> None:
    await state.clear()

    for path in paths.values():
        p = Path(path)

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

    paths = get_file_paths(title)

    await download_files(paths["video"], paths["audio"], v_stream, a_stream)

    if v_stream and a_stream:
        await process_and_send_video(call, state, paths)
    elif a_stream:
        await send_audio(call, paths["audio"])
    elif v_stream:
        await send_video(call, paths["video"])

    await clear_state_and_files(state, paths)
    await state.set_state(YoutubeStates.GET_URL)
