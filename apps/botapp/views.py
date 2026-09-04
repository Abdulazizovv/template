from __future__ import annotations

import logging
from typing import Any, Dict
from secrets import compare_digest

import redis as redis_lib
from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden, HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from aiogram.types import Update
from bot.dispatcher import dp
from bot.bot import bot

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def health_check(request: HttpRequest) -> JsonResponse:
    """Lightweight health endpoint for k8s/compose.

    Performs quick checks:
    - Database connection (simple cursor)
    - Redis ping (if redis extra available)
    - Bot token presence (does not call Telegram)
    """
    status: Dict[str, Any] = {"service": "django-bot", "ok": True}
    # DB check
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        status["db"] = "ok"
    except Exception as e:  # pragma: no cover - depends on env
        logger.exception("health_check: database check failed")
        status["ok"] = False
        status["db"] = f"error: {e}"

    # Redis check
    r = None
    try:
        r = redis_lib.from_url(settings.REDIS_URL)
        r.ping()
        status["redis"] = "ok"
    except Exception as e:  # pragma: no cover
        logger.exception("health_check: redis check failed")
        status["ok"] = False
        status["redis"] = f"error: {e}"
    finally:
        if r is not None:
            try:
                r.close()
            except Exception:
                logger.exception("health_check: failed to close redis connection")

    # Bot token presence
    status["bot_token"] = bool(getattr(bot, "token", None))

    http_status = 200 if status.get("ok") else 500
    return JsonResponse(status, status=http_status)


@require_http_methods(["GET"])
def bot_status(request: HttpRequest) -> JsonResponse:
    """Basic bot status without external API calls."""
    try:
        bot_info = {
            "status": "running",
            "has_token": bool(getattr(bot, "token", None)),
        }
        return JsonResponse(bot_info)
    except Exception as e:  # pragma: no cover
        logger.exception("bot_status: failed to build status")
        return JsonResponse({"status": "error", "error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
async def telegram_webhook(request: HttpRequest, token: str) -> HttpResponse:
    """Telegram webhook endpoint with security validation.

    Security:
    - Verifies bot token in URL path
    - Validates X-Telegram-Bot-Api-Secret-Token header
    - Rate limited by nginx (see nginx/default.conf)
    - Request body size limited (Nginx + MAX_BODY_BYTES)

    Args:
        request: Django HTTP request
        token: Bot token from URL path

    Returns:
        200 OK if processed
        403 Forbidden if validation fails
        400 Bad Request if invalid JSON or wrong Content-Type
        413 Payload Too Large if body exceeds limit
        500 Internal Server Error if processing fails
    """
    # 1) Path token must match actual bot token
    if not bot.token or not compare_digest(token, bot.token):
        return HttpResponseForbidden("Invalid token")

    # 2) Verify Telegram secret header
    webhook_secret = settings.TELEGRAM_WEBHOOK_SECRET
    secret_header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if webhook_secret and (not secret_header or not compare_digest(secret_header, webhook_secret)):
        return HttpResponseForbidden("Invalid secret token")

    # 3) Enforce JSON content type
    ctype = request.headers.get("Content-Type", "")
    if "application/json" not in ctype:
        return JsonResponse({"status": "bad_request", "error": "Content-Type must be application/json"}, status=400)

    # 4) Enforce body size
    max_body_bytes = settings.TELEGRAM_WEBHOOK_MAX_BODY
    try:
        content_length = int(request.META.get("CONTENT_LENGTH") or "0")
    except ValueError:
        content_length = 0
    if content_length and content_length > max_body_bytes:
        return JsonResponse({"status": "bad_request", "error": "Payload too large"}, status=413)

    # 5) Parse update
    try:
        raw_body = request.body
        if raw_body and len(raw_body) > max_body_bytes:
            return JsonResponse({"status": "bad_request", "error": "Payload too large"}, status=413)
        update = Update.model_validate_json(raw_body)
    except Exception as e:
        logger.warning("telegram_webhook: invalid update payload: %s", e)
        return JsonResponse({"status": "bad_request", "error": str(e)}, status=400)

    # 6) Hand over to aiogram dispatcher
    try:
        await dp.feed_update(bot=bot, update=update)
    except Exception as e:  # pragma: no cover - handler/runtime errors
        logger.exception("telegram_webhook: dispatcher failed to process update %s", update.update_id)
        return JsonResponse({"status": "error", "error": str(e)}, status=500)
    return JsonResponse({"status": "ok"})
