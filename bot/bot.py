from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from django.conf import settings

BOT_TOKEN = settings.BOT_TOKEN
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required")

# Create bot instance (Aiogram v3)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
