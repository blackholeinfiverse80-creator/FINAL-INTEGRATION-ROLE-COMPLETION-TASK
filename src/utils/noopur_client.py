import requests
from typing import Optional, Dict, Any
from config.config import NOOPUR_BASE_URL, NOOPUR_API_KEY


class NoopurClient:
    """Simple HTTP client for CreatorCore backend (Noopur).

    Methods used by the integrator:
      - generate (POST /generate) returns related_context
      - feedback (POST /feedback)
      - history (GET /history or /history/<topic>)
    """

    def __init__(self, base_url: str = NOOPUR_BASE_URL, api_key: Optional[str] = NOOPUR_API_KEY):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def generate(self, payload: Dict[str, Any], timeout: int = 5) -> Dict[str, Any]:
        url = f"{self.base_url}/generate"
        resp = self.session.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()

    def feedback(self, payload: Dict[str, Any], timeout: int = 5) -> Dict[str, Any]:
        url = f"{self.base_url}/feedback"
        resp = self.session.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return {"status": "ok"}

    def history(self, topic: Optional[str] = None, timeout: int = 5) -> Dict[str, Any]:
        if topic:
            url = f"{self.base_url}/history/{topic}"
        else:
            url = f"{self.base_url}/history"
        resp = self.session.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
