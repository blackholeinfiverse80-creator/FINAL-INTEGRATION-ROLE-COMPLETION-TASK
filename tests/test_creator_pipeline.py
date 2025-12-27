import pytest
from src.core.gateway import Gateway


class DummyNoopur:
    def generate(self, payload):
        return {"related_context": [
            {"id": "1", "topic": payload.get("topic"), "output_text": "prev 1", "similarity": 0.9},
            {"id": "2", "topic": payload.get("topic"), "output_text": "prev 2", "similarity": 0.8}
        ]}


class DummyAdapter:
    def get_context(self, user_id, limit=3):
        return [{"module": "sample_text", "timestamp": "2025-01-01T00:00:00", "request": {}, "response": {}}]

    def get_user_history(self, user_id):
        return []

    def store_interaction(self, user_id, request_data, response_data):
        return None


@pytest.fixture(autouse=True)
def monkey_noopur(monkeypatch):
    # Patch NoopurClient inside creator_routing to use DummyNoopur
    import creator_routing
    monkeypatch.setattr(creator_routing, 'NoopurClient', lambda: DummyNoopur())
    yield


def test_creator_prewarm_and_invoke():
    gw = Gateway()
    # swap memory adapter to dummy
    gw.memory = DummyAdapter()
    gw.creator_router = gw.creator_router.__class__(gw.memory)

    # simulate a creator request
    req = {"module": "creator", "intent": "generate", "user_id": "u1", "data": {"topic": "Space", "goal": "Tell a story", "type": "story"}}

    resp = gw.process_request(module="creator", intent="generate", user_id="u1", data=req['data'])
    # Gateway will route to CreatorAgent which returns canned success. Ensure response is dict with status
    assert isinstance(resp, dict)
    assert "status" in resp
