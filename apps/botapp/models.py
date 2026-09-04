from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel


class TelegramUser(BaseModel):
    """A Telegram user seen through the bot webhook."""

    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=64, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    is_blocked = models.BooleanField(default=False, verbose_name=_("Blocked the bot"))

    class Meta(BaseModel.Meta):
        verbose_name = _("Telegram user")
        verbose_name_plural = _("Telegram users")

    def __str__(self):
        return self.username or self.full_name or str(self.telegram_id)
