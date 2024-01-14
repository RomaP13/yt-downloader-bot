from typing import List

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_quality_inline_keyboard


async def edit_loading_message(call: CallbackQuery, bot: Bot, text: str) -> None:
    if call.message is not None:
        await bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=None,
        )


async def edit_quality_message(
    call: CallbackQuery, bot: Bot,
    state: FSMContext, resolutions: List[str]
) -> None:
    if call.message is not None:
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=get_quality_inline_keyboard(
                resolutions,
            )
        )
