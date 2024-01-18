import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command

from callbacks.media_selection import select_content, select_resolution
from callbacks.url_confirmation import handle_confirmation
from config_reader import config
from filters.is_youtube_url import IsYoutubeUrl
from handlers.basic import get_start, get_youtube_url, get_next_youtube_url
from utils.statesyoutube import YoutubeStates


FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


dp.message.register(get_start, Command("start"))
dp.message.register(get_youtube_url, YoutubeStates.GET_URL, IsYoutubeUrl())
dp.message.register(get_next_youtube_url, YoutubeStates.GET_OPTIONS,
                    IsYoutubeUrl())

dp.callback_query.register(select_resolution, F.data.startswith("res_"))
dp.callback_query.register(select_content, F.data.startswith("content_"))
dp.callback_query.register(handle_confirmation, F.data.startswith("confirm_"))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
