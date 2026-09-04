from django.conf import settings
from django.core.management.base import CommandError

from bot.bot import bot
from ._base import BotCommand


class Command(BotCommand):
    help = "Set Telegram webhook"

    def add_arguments(self, parser):
        parser.add_argument("--drop-pending", action="store_true", help="Drop pending updates on Telegram side")

    def handle(self, *args, **options):
        domain = settings.TELEGRAM_WEBHOOK_DOMAIN
        if not domain:
            raise CommandError("TELEGRAM_WEBHOOK_DOMAIN is not set")
        path = settings.TELEGRAM_WEBHOOK_PATH
        secret = settings.TELEGRAM_WEBHOOK_SECRET
        url = domain.rstrip("/") + path.rstrip("/") + f"/{bot.token}/"  # Final webhook url includes token

        self.stdout.write(f"Setting webhook to: {url}")

        async def _set():
            try:
                await bot.set_webhook(url=url, secret_token=secret, drop_pending_updates=options["drop_pending"])
                await bot.delete_my_commands()  # reset before re-setting
                from bot.utils.set_bot_commands import set_default_commands
                await set_default_commands(bot)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to set webhook: {e}"))
                raise

        self.run_async(_set())
        self.stdout.write(self.style.SUCCESS("Webhook set successfully."))
