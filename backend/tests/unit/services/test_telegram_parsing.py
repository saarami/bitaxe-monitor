import pytest

def test_parse_telegram_message_text():
    parse_update = None
    for path in ("app.services.telegram_parsing", "app.services.telegram_service", "app.services.telegram"):
        try:
            mod = __import__(path, fromlist=["*"])
            parse_update = getattr(mod, "parse_update", None) or getattr(mod, "parse_telegram_update", None)
            if parse_update:
                break
        except Exception:
            continue
    if parse_update is None:
        pytest.skip("Telegram parse_update function not found in app.services.*")

    update = {
        "update_id": 1,
        "message": {
            "message_id": 10,
            "chat": {"id": 123, "type": "private"},
            "text": "hello world",
        },
    }

    out = parse_update(update)
    assert out is not None
    if isinstance(out, dict):
        assert out.get("chat_id") == 123
        assert out.get("text") == "hello world"
    else:
        assert out[0] == 123
        assert out[1] == "hello world"
