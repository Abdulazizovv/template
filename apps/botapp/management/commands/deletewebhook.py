from bot.bot import bot
from ._base import BotCommand


class Command(BotCommand):
    help = "Delete Telegram webhook"

    def handle(self, *args, **options):
        self.run_async(bot.delete_webhook(drop_pending_updates=False))
        self.stdout.write(self.style.SUCCESS("Webhook deleted."))
