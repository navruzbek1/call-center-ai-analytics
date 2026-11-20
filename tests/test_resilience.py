import json
from types import SimpleNamespace

import pytest
from google.genai import errors as genai_errors

from callanalytics import resilience
from callanalytics.resilience import ContentBlockedError, call_with_retry, is_quota_exceeded_error, usage_to_dict


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    sleeps = []
    monkeypatch.setattr(resilience.time, "sleep", sleeps.append)
    return sleeps


def flaky(*failures, result="ok"):
    """Avval berilgan xatolarni ko'taradi, keyin natija qaytaradi."""
    queue = list(failures)

    def fn():
        if queue:
            raise queue.pop(0)
        return result
    return fn


def server_error():
    return genai_errors.ServerError(503, {"error": {"code": 503, "message": "overloaded", "status": "UNAVAILABLE"}})


def client_error(code):
    return genai_errors.ClientError(code, {"error": {"code": code, "message": "x", "status": "X"}})


def test_success_without_retry(no_sleep):
    assert call_with_retry(flaky()) == "ok"
    assert no_sleep == []


def test_server_error_retries_with_exponential_backoff(no_sleep):
    assert call_with_retry(flaky(server_error(), server_error()), base_delay=2.0) == "ok"
    assert no_sleep == [2.0, 4.0]


def test_rate_limit_429_is_retried(no_sleep):
    assert call_with_retry(flaky(client_error(429))) == "ok"
    assert len(no_sleep) == 1


def test_other_client_errors_are_raised_immediately(no_sleep):
    with pytest.raises(genai_errors.ClientError):
        call_with_retry(flaky(client_error(400)))
    assert no_sleep == []


def test_broken_json_is_retried(no_sleep):
    assert call_with_retry(flaky(json.JSONDecodeError("x", "{", 0))) == "ok"


def test_gives_up_after_max_retries():
    with pytest.raises(genai_errors.ServerError):
        call_with_retry(flaky(*[server_error() for _ in range(3)]), max_retries=3)


def test_quota_exceeded_detection():
    assert is_quota_exceeded_error(Exception("429 RESOURCE_EXHAUSTED"))
    assert is_quota_exceeded_error(Exception("Your project has exceeded its Spending Cap"))
    assert not is_quota_exceeded_error(Exception("500 internal"))


def test_content_blocked_error_keeps_reason():
    err = ContentBlockedError("PROHIBITED_CONTENT")
    assert err.block_reason == "PROHIBITED_CONTENT"
    assert "PROHIBITED_CONTENT" in str(err)


def test_usage_to_dict():
    usage = SimpleNamespace(
        prompt_token_count=1000, candidates_token_count=200, thoughts_token_count=50,
        cached_content_token_count=None, total_token_count=1250,
        prompt_tokens_details=[SimpleNamespace(modality="AUDIO", token_count=800),
                               SimpleNamespace(modality="TEXT", token_count=200)],
        candidates_tokens_details=None,
    )
    out = usage_to_dict(usage)
    assert out["total_token_count"] == 1250
    assert out["modality_breakdown"] == {"prompt_tokens_details:AUDIO": 800, "prompt_tokens_details:TEXT": 200}
    assert usage_to_dict(None) == {}
