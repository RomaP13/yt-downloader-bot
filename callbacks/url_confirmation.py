import logging

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.basic import get_youtube_url
from utils.message_utils import edit_message
from utils.statesyoutube import YoutubeStates


async def handle_confirmation(call: CallbackQuery, bot: Bot,
                              state: FSMContext) -> None:
    await bot.answer_callback_query(call.id)

    assert call.data is not None, "'call.data' is None in handle_confirmation"
    answer = call.data.split("_")[1]

    data = await state.get_data()
    message = data.get("bot_message")

    try:
        if answer in ["yes", "no"]:
            if message is not None:
                await edit_message(
                    bot, message.chat.id, message.message_id,
                    "Downloading stopped."
                )

        if answer == "yes":
            await get_youtube_url(call, bot, state)
        elif answer == "no":
            assert (
                call.message is not None
            ), "'call.message' is None in handle_confirmation"

            await edit_message(
                bot,
                call.from_user.id,
                call.message.message_id,
                "Please don't send multiple links. Try again.",
            )

            await state.clear()
            await state.set_state(YoutubeStates.GET_URL)
        else:
            logging.error("Unexpected condition in handle_confirmation.")
    except Exception as e:
        logging.exception("An error occurred in handle_confirmation: %s",
                          str(e))
