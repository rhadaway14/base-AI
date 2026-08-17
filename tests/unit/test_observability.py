from app_observability.logging import redact


def test_sensitive_log_fields_are_redacted() -> None:
    event = redact({"event": "x", "password": "secret", "content": "private"})
    assert event["password"] == "[REDACTED]"
    assert event["content"] == "[REDACTED]"
    assert event["event"] == "x"
