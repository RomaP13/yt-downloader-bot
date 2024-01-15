import logging

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.message_utils import edit_loading_message


async def handle_confirmation(call: CallbackQuery, bot: Bot,
                              state: FSMContext) -> None:
    await bot.answer_callback_query(call.id)

    assert call.data is not None, "'call.data' is None in handle_confirmation"
    answer = call.data.split("_")[1]

    data = await state.get_data()
    message = data.get("bot_message")

    try:
        if answer == "yes":
            assert (
                message is not None
            ), "'message' is None in handle_confirmation"

            await edit_loading_message(
                bot, message.chat.id, message.message_id,
                "TEST: OLD MESSAGE CHANGED"
            )
        elif answer == "no":
            assert (
                call.message is not None
            ), "'call.message' is None in handle_confirmation"

            await edit_loading_message(
                bot,
                call.from_user.id,
                call.message.message_id,
                "TEST: NEW MESSAGE CHANGED",
            )
        else:
            logging.error("Unexpected condition in handle_confirmation.")
    except Exception as e:
        logging.exception("An error occurred in handle_confirmation: %s",
                          str(e))
