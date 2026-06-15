import json
import re

from fastapi.testclient import TestClient

from app.logging_config import scrub_event
from app.main import app


def test_correlation_id_is_generated_and_returned() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    request_id = response.headers["x-request-id"]
    assert re.fullmatch(r"req-[0-9a-f]{8}", request_id)
    assert response.headers["x-response-time-ms"].isdigit()


def test_correlation_id_header_is_preserved() -> None:
    client = TestClient(app)

    response = client.get("/health", headers={"x-request-id": "req-deadbeef"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req-deadbeef"


def test_chat_logs_are_enriched_and_scrubbed(tmp_path, monkeypatch) -> None:
    log_path = tmp_path / "logs.jsonl"
    monkeypatch.setenv("LOG_PATH", str(log_path))
    monkeypatch.setenv("APP_ENV", "test")
    client = TestClient(app)

    response = client.post(
        "/chat",
        headers={"x-request-id": "req-1234abcd"},
        json={
            "user_id": "student@example.com",
            "session_id": "session-01",
            "feature": "qa",
            "message": "My email is student@example.com and card is 4111 1111 1111 1111",
        },
    )

    assert response.status_code == 200
    assert response.json()["correlation_id"] == "req-1234abcd"
    records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    api_records = [record for record in records if record.get("service") == "api"]
    assert api_records
    assert all(record["correlation_id"] == "req-1234abcd" for record in api_records)
    assert all(record["env"] == "test" for record in api_records)
    assert all(record["session_id"] == "session-01" for record in api_records)
    assert all(record["feature"] == "qa" for record in api_records)
    assert all(record["model"] for record in api_records)
    assert all("user_id_hash" in record for record in api_records)
    raw_logs = "\n".join(json.dumps(record) for record in records)
    assert "student@example.com" not in raw_logs
    assert "4111" not in raw_logs
    assert "[REDACTED_EMAIL]" in raw_logs
    assert "[REDACTED_CREDIT_CARD]" in raw_logs


def test_scrub_event_handles_nested_payload() -> None:
    event = {
        "event": "payment for student@example.com",
        "payload": {
            "message": "Call 090 123 4567",
            "nested": {"card": "4111-1111-1111-1111"},
            "items": ["CCCD 012345678901"],
        },
    }

    scrubbed = scrub_event(None, "info", event)
    raw = json.dumps(scrubbed)

    assert "student@example.com" not in raw
    assert "090 123" not in raw
    assert "4111" not in raw
    assert "012345678901" not in raw
    assert "[REDACTED_EMAIL]" in raw
    assert "[REDACTED_PHONE_VN]" in raw
    assert "[REDACTED_CREDIT_CARD]" in raw
    assert "[REDACTED_CCCD]" in raw
