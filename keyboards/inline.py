from typing import List

from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Only video", callback_data="content_video")
    keyboard_builder.button(text="Only audio", callback_data="content_audio")
    keyboard_builder.button(text="Video and audio",
                            callback_data="content_both")

    return keyboard_builder.as_markup()


def get_quality_inline_keyboard(resolutions: List[str]) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()

    for res in resolutions:
        keyboard_builder.button(text=res, callback_data=f"quality_{res}")

    return keyboard_builder.as_markup()


def get_confirm_download_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Yes", callback_data="confirm_yes")
    keyboard_builder.button(text="No", callback_data="confirm_no")

    return keyboard_builder.as_markup()
