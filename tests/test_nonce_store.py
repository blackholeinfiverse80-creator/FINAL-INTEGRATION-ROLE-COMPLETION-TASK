from src.db.nonce_store import NonceStore
import time


def test_nonce_store_basic():
    ns = NonceStore(db_path=":memory:")
    nonce = "test-nonce-1"
    assert ns.use_nonce(nonce) is True
    # reuse returns False
    assert ns.use_nonce(nonce) is False


def test_nonce_store_isolated():
    ns = NonceStore(db_path=":memory:")
    # different nonces are accepted
    assert ns.use_nonce("n1") is True
    assert ns.use_nonce("n2") is True
