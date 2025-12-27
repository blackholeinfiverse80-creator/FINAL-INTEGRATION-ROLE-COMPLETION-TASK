from src.utils.sspl_dependency import require_sspl
from src.utils import sspl, sspl_dependency
from src.db.nonce_store import NonceStore
import json
import time
import asyncio
from starlette.datastructures import URL


class DummyRequest:
    def __init__(self, json_body=None, headers=None, path="/protected"):
        self._json = json_body
        self.headers = headers or {}
        class _U:
            def __init__(self, path):
                self.path = path
                self.query_params = {}
        self.url = _U(path)

    async def json(self):
        if self._json is None:
            raise ValueError("no json")
        return self._json


def run_dep(req):
    return asyncio.run(require_sspl(req))


def test_middleware_allows_when_pynacl_missing(monkeypatch):
    # Simulate PyNaCl not installed
    monkeypatch.setattr(sspl, "VerifyKey", None)
    ts = str(time.time())
    body = {"timestamp": ts, "nonce": "n-1"}
    # ensure a fresh nonce store for this test
    monkeypatch.setattr(sspl_dependency, "nonce_store", NonceStore(db_path=":memory:"))
    req = DummyRequest(json_body=body)
    assert run_dep(req) is True


def test_middleware_rejects_stale_timestamp(monkeypatch):
    monkeypatch.setattr(sspl, "VerifyKey", None)
    ts = str(time.time() - 10000)
    body = {"timestamp": ts, "nonce": "n-2"}
    monkeypatch.setattr(sspl_dependency, "nonce_store", NonceStore(db_path=":memory:"))
    req = DummyRequest(json_body=body)
    try:
        run_dep(req)
        assert False, "expected exception"
    except Exception as e:
        assert "Stale" in str(e) or "Stale timestamp" in str(e) or "401" in str(e)


def test_middleware_replays_are_blocked(monkeypatch):
    monkeypatch.setattr(sspl, "VerifyKey", None)
    ts = str(time.time())
    body = {"timestamp": ts, "nonce": "n-3"}
    monkeypatch.setattr(sspl_dependency, "nonce_store", NonceStore(db_path=":memory:"))
    req1 = DummyRequest(json_body=body)
    assert run_dep(req1) is True
    req2 = DummyRequest(json_body=body)
    try:
        run_dep(req2)
        assert False, "expected replay exception"
    except Exception as e:
        assert "Nonce already used" in str(e) or "409" in str(e)
