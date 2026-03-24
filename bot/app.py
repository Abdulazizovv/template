import asyncio

from bot.bot import bot
from bot.dispatcher import create_dispatcher
from bot.utils.notify_admins import on_startup_notify
from bot.utils.set_bot_commands import set_default_commands


async def main() -> None:
    dp = create_dispatcher()
    await set_default_commands(bot)
    await on_startup_notify(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
