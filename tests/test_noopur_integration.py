import pytest
import requests
from unittest.mock import Mock, patch
from src.utils.noopur_client import NoopurClient


class TestNoopurClient:
    """Test suite for NoopurClient integration."""

    def setup_method(self):
        """Setup test client."""
        self.client = NoopurClient(base_url="http://test-server", api_key="test-key")

    def test_client_initialization(self):
        """Test client initialization with default and custom values."""
        # Test with defaults
        default_client = NoopurClient()
        assert default_client.base_url == "http://localhost:5001"
        
        # Test with custom values
        custom_client = NoopurClient("http://custom", "custom-key")
        assert custom_client.base_url == "http://custom"
        assert custom_client.api_key == "custom-key"

    @patch('requests.Session.post')
    def test_generate_success(self, mock_post):
        """Test successful generate request."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "related_context": [
                {"id": "1", "topic": "test", "output_text": "result", "similarity": 0.9}
            ]
        }
        mock_post.return_value = mock_response

        payload = {"topic": "test", "goal": "generate"}
        result = self.client.generate(payload)

        mock_post.assert_called_once_with(
            "http://test-server/generate", 
            json=payload, 
            timeout=5
        )
        assert "related_context" in result

    @patch('requests.Session.post')
    def test_feedback_success(self, mock_post):
        """Test successful feedback request."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "received"}
        mock_post.return_value = mock_response

        payload = {"feedback": "positive", "session_id": "123"}
        result = self.client.feedback(payload)

        mock_post.assert_called_once_with(
            "http://test-server/feedback", 
            json=payload, 
            timeout=5
        )
        assert result["status"] == "received"

    @patch('requests.Session.get')
    def test_history_without_topic(self, mock_get):
        """Test history request without topic."""
        mock_response = Mock()
        mock_response.json.return_value = {"history": []}
        mock_get.return_value = mock_response

        result = self.client.history()

        mock_get.assert_called_once_with("http://test-server/history", timeout=5)
        assert "history" in result

    @patch('requests.Session.get')
    def test_history_with_topic(self, mock_get):
        """Test history request with specific topic."""
        mock_response = Mock()
        mock_response.json.return_value = {"history": [{"topic": "test"}]}
        mock_get.return_value = mock_response

        result = self.client.history("test")

        mock_get.assert_called_once_with("http://test-server/history/test", timeout=5)
        assert result["history"][0]["topic"] == "test"

    @patch('requests.Session.post')
    def test_request_timeout(self, mock_post):
        """Test timeout handling."""
        mock_post.side_effect = requests.Timeout("Request timed out")

        with pytest.raises(requests.Timeout):
            self.client.generate({"topic": "test"})

    @patch('requests.Session.post')
    def test_http_error(self, mock_post):
        """Test HTTP error handling."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_post.return_value = mock_response

        with pytest.raises(requests.HTTPError):
            self.client.generate({"topic": "test"})

    @patch('requests.Session.post')
    def test_feedback_json_decode_error(self, mock_post):
        """Test feedback with invalid JSON response."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response

        result = self.client.feedback({"feedback": "test"})
        assert result == {"status": "ok"}


class TestNoopurIntegration:
    """Integration tests with mock server responses."""

    @patch('requests.Session.post')
    def test_full_generate_workflow(self, mock_post):
        """Test complete generate workflow."""
        client = NoopurClient("http://localhost:5001", "test-api-key")
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "related_context": [
                {
                    "id": "ctx_1",
                    "topic": "AI",
                    "output_text": "AI is transforming industries",
                    "similarity": 0.95
                },
                {
                    "id": "ctx_2", 
                    "topic": "AI",
                    "output_text": "Machine learning applications",
                    "similarity": 0.87
                }
            ]
        }
        mock_post.return_value = mock_response

        payload = {
            "topic": "AI",
            "goal": "educational content",
            "type": "article"
        }

        result = client.generate(payload, timeout=10)
        
        # Verify request
        mock_post.assert_called_once_with(
            "http://localhost:5001/generate",
            json=payload,
            timeout=10
        )
        
        # Verify response structure
        assert "related_context" in result
        assert len(result["related_context"]) == 2
        assert result["related_context"][0]["similarity"] == 0.95

    @patch('requests.Session.post')
    @patch('requests.Session.get')
    def test_generate_feedback_history_flow(self, mock_get, mock_post):
        """Test complete workflow: generate -> feedback -> history."""
        client = NoopurClient()

        # Mock generate response
        generate_response = Mock()
        generate_response.json.return_value = {
            "related_context": [{"id": "1", "topic": "test"}]
        }
        
        # Mock feedback response
        feedback_response = Mock()
        feedback_response.json.return_value = {"status": "received"}
        
        # Mock history response
        history_response = Mock()
        history_response.json.return_value = {
            "history": [{"session_id": "123", "topic": "test"}]
        }

        mock_post.side_effect = [generate_response, feedback_response]
        mock_get.return_value = history_response

        # Execute workflow
        gen_result = client.generate({"topic": "test"})
        feedback_result = client.feedback({"session_id": "123", "rating": 5})
        history_result = client.history("test")

        # Verify all calls were made
        assert mock_post.call_count == 2
        assert mock_get.call_count == 1
        
        # Verify results
        assert "related_context" in gen_result
        assert feedback_result["status"] == "received"
        assert "history" in history_result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])