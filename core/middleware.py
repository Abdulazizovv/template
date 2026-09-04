from __future__ import annotations

import re
import uuid
from django.http import HttpRequest, HttpResponse

from .logging_utils import request_id_var

_VALID_REQUEST_ID = re.compile(r"^[A-Za-z0-9\-]{1,64}$")


class RequestIdMiddleware:
    """Attach request_id to each request and response."""

    header_name = "X-Request-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        incoming = request.headers.get(self.header_name)
        req_id = incoming if incoming and _VALID_REQUEST_ID.match(incoming) else uuid.uuid4().hex
        token = request_id_var.set(req_id)
        try:
            response = self.get_response(request)
            response[self.header_name] = req_id
            return response
        finally:
            request_id_var.reset(token)
