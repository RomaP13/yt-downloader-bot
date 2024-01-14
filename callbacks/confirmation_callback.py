from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.message_utils import edit_loading_message


async def handle_confirmation(call: CallbackQuery, bot: Bot,
                              state: FSMContext) -> None:
    await bot.answer_callback_query(call.id)

    if call.data is None:
        return

    answer = call.data.split("_")[1]

    if answer == "yes":
        data = await state.get_data()
        message = data.get("message")
        await edit_loading_message(message, bot, "TEST: OLD MESSAGE CHANGED")
    elif answer == "no":
        await edit_loading_message(call, bot, "TEST: NEW MESSAGE CHANGED")
