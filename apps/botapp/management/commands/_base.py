import asyncio

from django.core.management.base import BaseCommand

from bot.bot import bot


class BotCommand(BaseCommand):
    """Base command for one-off bot operations. Ensures the shared aiogram
    `Bot` session is always closed after the coroutine finishes or raises."""

    def run_async(self, coro):
        async def _runner():
            try:
                return await coro
            finally:
                await bot.session.close()

        return asyncio.run(_runner())
