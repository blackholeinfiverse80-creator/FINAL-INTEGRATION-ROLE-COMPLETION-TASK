import time
import base64
import json
from nacl.signing import SigningKey
from src.utils.sspl import verify_signature, SSPL
from src.utils.sspl_dependency import require_sspl
from src.db.nonce_store import NonceStore


def sign_message(signing_key: SigningKey, body: dict) -> (str, str):
    b = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    sig = signing_key.sign(b).signature
    pub = signing_key.verify_key
    return base64.b64encode(sig).decode("utf-8"), base64.b64encode(pub.encode()).decode("utf-8")


def test_signature_verification_and_middleware(monkeypatch):
    sk = SigningKey.generate()
    ts = str(time.time())
    body = {"timestamp": ts, "nonce": "s-n-1"}
    sig_b64, pub_b64 = sign_message(sk, body)

    # Direct signature verify
    ok = SSPL.verify_signature(pub_b64, json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8"), sig_b64)
    assert ok is True

    # Now call middleware with real VerifyKey available
    monkeypatch.setattr("src.utils.sspl.VerifyKey", __import__("nacl.signing").signing.VerifyKey)
    from src.utils import sspl_dependency
    monkeypatch.setattr(sspl_dependency, "nonce_store", NonceStore(db_path=":memory:"))

    class DummyReq:
        def __init__(self, json_body, headers=None):
            self._json = json_body
            self.headers = headers or {"X-SSPL-Signature": sig_b64, "X-SSPL-PubId": pub_b64}
            class _U:
                def __init__(self):
                    self.path = "/protected"
                    self.query_params = {}
            self.url = _U()

        async def json(self):
            return self._json

    req = DummyReq(body)
    # will raise if verification fails
    import asyncio
    asyncio.get_event_loop().run_until_complete(require_sspl(req))
