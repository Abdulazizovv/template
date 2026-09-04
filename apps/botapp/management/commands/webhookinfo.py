from bot.bot import bot
from ._base import BotCommand


class Command(BotCommand):
    help = "Show current Telegram webhook info"

    def handle(self, *args, **options):
        async def _info():
            info = await bot.get_webhook_info()
            return info.model_dump()

        data = self.run_async(_info())
        self.stdout.write(self.style.SUCCESS("Current webhook info:"))
        for k, v in data.items():
            self.stdout.write(f" - {k}: {v}")
