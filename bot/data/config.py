from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN", default=None)  # Bot token
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required")
ADMINS = env.list("ADMINS", default=[])  # adminlar ro'yxati
