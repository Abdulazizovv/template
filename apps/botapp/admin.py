from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "full_name", "is_blocked", "created_at")
    list_filter = ("is_blocked",)
    search_fields = ("telegram_id", "username", "full_name")
    readonly_fields = ("id", "created_at", "updated_at")
