from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, Update

from app.features.telegram.service import VerificationService


def build_dispatcher(verification_service: VerificationService) -> Dispatcher:
    router = Router()

    @router.message(CommandStart(deep_link=True))
    async def handle_start(message: Message, command: CommandStart) -> None:
        if command.args is None:
            await message.answer("Verification link is missing or invalid.")
            return

        intent = await verification_service.attach_user_session(message.from_user.id, command.args)
        if intent is None:
            await message.answer("Verification link expired or was not found.")
            return

        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Share contact", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await message.answer(
            "Share your Telegram contact to confirm the phone number used during signup.",
            reply_markup=keyboard,
        )

    @router.message(F.contact)
    async def handle_contact(message: Message) -> None:
        if message.contact is None or message.from_user is None:
            await message.answer("Contact payload is missing.")
            return

        if message.contact.user_id != message.from_user.id:
            await message.answer("Please share your own Telegram contact.")
            return

        intent = await verification_service.confirm_contact(message.from_user.id, message.contact.phone_number)
        if intent is None:
            await message.answer("Verification session expired. Please restart the signup flow.")
            return

        if intent.status == "mismatch":
            await message.answer("The shared phone number does not match the signup phone number.")
            return

        await message.answer(f"Your CRM Workroom verification code: {intent.code}")

    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    return dispatcher


async def handle_update(bot: Bot, dispatcher: Dispatcher, update: dict) -> None:
    telegram_update = Update.model_validate(update)
    await dispatcher.feed_update(bot, telegram_update)