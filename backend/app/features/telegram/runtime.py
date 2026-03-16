import asyncio
import contextlib

from aiogram import Bot
from fastapi import FastAPI
from redis.asyncio import Redis

from app.config.settings import Settings
from app.features.telegram.bot import build_dispatcher
from app.features.telegram.service import VerificationService
from app.features.telegram.storage import RedisVerificationStore


async def setup_telegram_runtime(app: FastAPI, settings: Settings) -> None:
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    store = RedisVerificationStore(redis=redis, ttl_seconds=settings.verification_ttl_seconds)
    verification_service = VerificationService(
        store=store,
        bot_username=settings.telegram_bot_username,
        ttl_seconds=settings.verification_ttl_seconds,
    )

    app.state.redis = redis
    app.state.verification_service = verification_service
    app.state.bot = None
    app.state.dispatcher = None
    app.state.polling_task = None

    if not settings.telegram_bot_token:
        return

    bot = Bot(token=settings.telegram_bot_token)
    dispatcher = build_dispatcher(verification_service)

    app.state.bot = bot
    app.state.dispatcher = dispatcher

    if settings.telegram_delivery_mode == "polling":
        await bot.delete_webhook(drop_pending_updates=True)
        app.state.polling_task = asyncio.create_task(dispatcher.start_polling(bot))


async def shutdown_telegram_runtime(app: FastAPI) -> None:
    polling_task = getattr(app.state, "polling_task", None)
    if polling_task is not None:
        polling_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await polling_task

    bot = getattr(app.state, "bot", None)
    if bot is not None:
        await bot.session.close()

    redis = getattr(app.state, "redis", None)
    if redis is not None:
        await redis.aclose()
