from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env
try:
    from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
except Exception:  # pragma: no cover - optional
    RedisStorage = None  # type: ignore[assignment]
    DefaultKeyBuilder = None  # type: ignore[assignment]
from .routers import register_routers


def create_dispatcher() -> Dispatcher:
    env = Env()
    env.read_env()
    storage = MemoryStorage()
    redis_url = env.str("REDIS_URL", default="")
    if RedisStorage is not None and redis_url:
        storage = RedisStorage.from_url(
            redis_url,
            key_builder=DefaultKeyBuilder(with_bot_id=True),
        )
    dp = Dispatcher(storage=storage)
    register_routers(dp)
    return dp


# A global dispatcher instance (can be imported where needed)
dp = create_dispatcher()
