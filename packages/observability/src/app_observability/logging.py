from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from app_observability.correlation import get_correlation_id

SENSITIVE_KEYS = frozenset({"password", "token", "secret", "api_key", "authorization", "content"})


def redact(event: dict[str, object]) -> dict[str, object]:
    cleaned = dict(event)
    for key in list(cleaned):
        if key.lower() in SENSITIVE_KEYS:
            cleaned[key] = "[REDACTED]"
    return cleaned


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "event": record.getMessage(),
        }
        if correlation_id := get_correlation_id():
            payload["correlation_id"] = correlation_id
        return json.dumps(redact(payload), separators=(",", ":"))


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level.upper())
