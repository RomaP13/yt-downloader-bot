import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsYoutubeUrl(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if bool(re.search(r"(https?://)?(www\.)?youtube\.\S+", message.text)):
            return True
        else:
            return False
