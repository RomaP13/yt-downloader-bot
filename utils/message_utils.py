from aiogram import Bot
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


async def edit_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None
) -> None:
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
        )
    except Exception as e:
        print(f"Error editing loading message: {e}")
