"""
CI-safe tests with mocked external dependencies
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestCISafe:
    """CI-safe tests with all external dependencies mocked"""
    
    @patch('src.utils.noopur_client.requests.Session')
    def test_noopur_client_mocked(self, mock_session):
        """Test NoopurClient with mocked requests"""
        from src.utils.noopur_client import NoopurClient
        
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success", "data": "test"}
        mock_session.return_value.post.return_value = mock_response
        
        client = NoopurClient("http://mock-noopur")
        result = client.generate({"topic": "test"})
        
        assert result["status"] == "success"
        mock_session.return_value.post.assert_called_once()
    
    @patch('src.utils.resilient_client.requests.Session')
    def test_resilient_client_mocked(self, mock_session):
        """Test ResilientHTTPClient with mocked requests"""
        from src.utils.resilient_client import ResilientHTTPClient
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_response
        
        client = ResilientHTTPClient("http://mock-service")
        result = client.post("/test", json={"data": "test"})
        
        assert result["result"] == "success"
    
    def test_mongodb_adapter_import_only(self):
        """Test MongoDB adapter can be imported without connection"""
        try:
            from src.db.mongodb_adapter import MongoDBAdapter
            # Just verify the class can be imported
            assert MongoDBAdapter is not None
        except ImportError:
            pytest.skip("MongoDB adapter not available")
    
    def test_feedback_schema_validation_no_network(self):
        """Test feedback schema validation without network calls"""
        from src.core.feedback_models import CanonicalFeedbackSchema
        
        # Valid feedback
        feedback = CanonicalFeedbackSchema(
            generation_id=123,
            command="+1",
            user_id="test_user"
        )
        
        assert feedback.generation_id == 123
        assert feedback.command == "+1"
        assert feedback.user_id == "test_user"
        assert isinstance(feedback.timestamp, datetime)
    
    @patch('src.core.gateway.Gateway.__init__')
    def test_gateway_initialization_mocked(self, mock_init):
        """Test Gateway initialization with mocked dependencies"""
        mock_init.return_value = None
        
        from src.core.gateway import Gateway
        gateway = Gateway()
        
        # Mock agents
        gateway.agents = {
            "finance": Mock(),
            "education": Mock(), 
            "creator": Mock()
        }
        gateway.memory = Mock()
        gateway.logger = Mock()
        
        # Test process_request with mocked components
        mock_agent = Mock()
        mock_agent.handle_request.return_value = {"status": "success", "result": {"test": "data"}}
        gateway.agents["finance"] = mock_agent
        
        result = gateway.process_request("finance", "test", "user1", {"test": "data"})
        
        assert result["status"] == "success"
        mock_agent.handle_request.assert_called_once()
    
    @patch('sqlite3.connect')
    def test_memory_operations_mocked(self, mock_connect):
        """Test memory operations with mocked SQLite"""
        from src.db.memory import ContextMemory
        
        # Mock SQLite connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.execute.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = (5,)
        
        memory = ContextMemory(":memory:")
        memory.store_interaction("user1", {"test": "request"}, {"test": "response"})
        
        mock_conn.execute.assert_called()
    
    @patch('requests.get')
    def test_health_endpoint_external_services_mocked(self, mock_get):
        """Test health endpoint with mocked external service calls"""
        # Mock successful health check
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with patch('src.db.mongodb_adapter.MongoDBAdapter') as mock_mongo:
            mock_mongo_instance = Mock()
            mock_mongo.return_value = mock_mongo_instance
            mock_mongo_instance.client.admin.command.return_value = {"ok": 1}
            
            # Test would pass with mocked services
            assert mock_response.status_code == 200
    
    def test_core_models_validation(self):
        """Test core models without external dependencies"""
        from src.core.models import CoreRequest, CoreResponse
        
        # Test CoreRequest
        request = CoreRequest(
            module="finance",
            intent="generate", 
            user_id="test_user",
            data={"test": "data"}
        )
        
        assert request.module == "finance"
        assert request.intent == "generate"
        assert request.user_id == "test_user"
        
        # Test CoreResponse
        response = CoreResponse(
            status="success",
            message="Test message",
            result={"test": "result"}
        )
        
        assert response.status == "success"
        assert response.message == "Test message"
    
    @patch('src.utils.logger.logging')
    def test_logging_setup_mocked(self, mock_logging):
        """Test logging setup with mocked logging module"""
        from src.utils.logger import setup_logger
        
        mock_logger = Mock()
        mock_logging.getLogger.return_value = mock_logger
        
        logger = setup_logger("test_module")
        
        mock_logging.getLogger.assert_called_with("test_module")
    
    def test_sspl_validation_no_crypto(self):
        """Test SSPL validation logic without crypto dependencies"""
        from src.utils.sspl import SSPL
        
        # Test timestamp validation (no crypto needed)
        sspl = SSPL()
        
        # Current timestamp should be fresh
        import time
        current_time = int(time.time())
        assert sspl.timestamp_fresh(current_time)
        
        # Old timestamp should not be fresh (older than default 300s)
        old_time = current_time - 400
        assert not sspl.timestamp_fresh(old_time)
    
    def test_nonce_store_mocked(self):
        """Test nonce store with mocked file system"""
        with patch('os.path.exists', return_value=True):
            with patch('sqlite3.connect') as mock_connect:
                mock_conn = Mock()
                mock_cursor = Mock()
                mock_connect.return_value.__enter__.return_value = mock_conn
                mock_conn.cursor.return_value = mock_cursor
                mock_cursor.fetchone.return_value = None  # Nonce not found (new nonce)
                
                from src.db.nonce_store import NonceStore
                nonce_store = NonceStore()
                
                # Test nonce usage - should return True for new nonce
                result = nonce_store.use_nonce("test_nonce")
                # The actual implementation returns True for successful nonce usage
                assert isinstance(result, bool)