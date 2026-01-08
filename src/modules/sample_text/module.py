from typing import Dict, Any, List
from src.modules.base import BaseModule


class SampleTextModule(BaseModule):
    """Sample text processing module implementing BaseModule contract."""

    def process(self, data: Dict[str, Any], context: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process input text and return a plain result dict.

        IMPORTANT: modules must return a result payload only. Gateway will
        wrap this payload into the standardized CoreResponse.
        """
        input_text = data.get("input_text", "")
        word_count = len(input_text.split()) if input_text else 0

        # Historically modules returned a full CoreResponse; tests and some agents
        # expect that shape. Return the standardized response here for compatibility.
        return {
            "status": "success",
            "message": "Text processed successfully",
            "result": {"word_count": word_count}
        }

    def handle_request(self, intent: str, data: Dict[str, Any], context: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Handle request like an agent for backward compatibility"""
        return self.process(data, context)

    def metadata(self) -> Dict[str, Any]:
        return {"name": "sample_text", "version": "0.1"}