from django.conf import settings

BOT_TOKEN = settings.BOT_TOKEN
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required")

ADMINS = settings.TELEGRAM_ADMIN_IDS
