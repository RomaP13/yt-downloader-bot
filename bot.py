import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command

from callback import select_content, select_quality
from callbacks.confirmation_callback import handle_confirmation
from config_reader import config
from filters.is_youtube_url import IsYoutubeUrl
from handlers.basic import get_start, get_youtube_url, get_another_youtube_url
from utils.statesyoutube import YoutubeStates


logging.basicConfig(level=logging.INFO)
logging.debug("Handling start command")

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


dp.message.register(get_start, Command("start"))
dp.message.register(get_youtube_url, YoutubeStates.GET_URL, IsYoutubeUrl())
dp.message.register(get_another_youtube_url, YoutubeStates.GET_OPTIONS, IsYoutubeUrl())

dp.callback_query.register(select_quality, F.data.startswith("quality_"))
dp.callback_query.register(select_content, F.data.startswith("content_"))
dp.callback_query.register(handle_confirmation, F.data.startswith("confirm_"))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
