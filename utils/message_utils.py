from typing import List

from aiogram import Bot

from keyboards.inline import get_resolution_inline_keyboard


async def edit_loading_message(
    bot: Bot, chat_id: int, message_id: int, text: str
) -> None:
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=None,
        )
    except Exception as e:
        print(f"Error editing loading message: {e}")


async def edit_resolution_message(
    bot: Bot, chat_id: int, message_id: int, resolutions: List[str]
) -> None:
    try:
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=get_resolution_inline_keyboard(
                resolutions,
            ),
        )
    except Exception as e:
        print(f"Error editing resolution message: {e}")
