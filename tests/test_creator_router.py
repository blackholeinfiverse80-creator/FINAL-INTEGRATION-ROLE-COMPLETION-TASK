"""
Test CreatorRouter prewarm logic and functionality
Tests the routing and context preparation logic
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from creator_routing import CreatorRouter
from src.db.memory_adapter import MemoryAdapter

class TestCreatorRouter:
    """Test suite for CreatorRouter functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test components"""
        self.memory_adapter = MemoryAdapter()
        self.test_user_id = "test_user_router"
    
    def test_router_initialization_with_noopur(self):
        """Test router initializes with Noopur integration"""
        # Test with Noopur enabled
        with patch.dict(os.environ, {"INTEGRATOR_USE_NOOPUR": "true"}):
            router = CreatorRouter(self.memory_adapter)
            assert router.memory == self.memory_adapter
            # Noopur client should be initialized if available
    
    def test_router_initialization_without_noopur(self):
        """Test router initializes without Noopur integration"""
        # Test with Noopur disabled
        with patch.dict(os.environ, {"INTEGRATOR_USE_NOOPUR": "false"}):
            router = CreatorRouter(self.memory_adapter)
            assert router.memory == self.memory_adapter
            assert router.noopur is None
    
    def test_prewarm_with_noopur_success(self):
        """Test prewarm logic with successful Noopur call"""
        router = CreatorRouter(self.memory_adapter)
        
        # Mock successful Noopur response
        mock_noopur_response = {
            "related_context": [
                {"text": "Related content 1", "score": 0.9},
                {"text": "Related content 2", "score": 0.8},
                {"text": "Related content 3", "score": 0.7}
            ]
        }
        
        # Mock Noopur client
        router.noopur = Mock()
        router.noopur.generate.return_value = mock_noopur_response
        
        input_data = {
            "topic": "AI Technology",
            "goal": "Create tutorial",
            "type": "article"
        }
        
        # Test prewarm
        result = router.prewarm_and_prepare("generate", self.test_user_id, input_data)
        
        # Verify context was added
        assert "related_context" in result
        assert len(result["related_context"]) == 3
        assert result["related_context"][0]["score"] == 0.9
        
        # Verify original data preserved
        assert result["topic"] == "AI Technology"
        assert result["goal"] == "Create tutorial"
    
    def test_prewarm_with_noopur_failure(self):
        """Test prewarm logic with Noopur failure (fallback to memory)"""
        router = CreatorRouter(self.memory_adapter)
        
        # Mock failing Noopur client
        router.noopur = Mock()
        router.noopur.generate.side_effect = Exception("Noopur unavailable")
        
        # Store some memory context
        self.memory_adapter.store_interaction(
            self.test_user_id,
            {"topic": "Memory Test", "module": "creator"},
            {"status": "success", "content": "memory content"}
        )
        
        input_data = {
            "topic": "Test Topic",
            "goal": "Test Goal",
            "type": "test"
        }
        
        # Test prewarm with failure
        result = router.prewarm_and_prepare("generate", self.test_user_id, input_data)
        
        # Should fallback gracefully and return original data
        assert result["topic"] == "Test Topic"
        assert result["goal"] == "Test Goal"
        
        # May have memory context if available
        if "related_context" in result:
            assert isinstance(result["related_context"], list)
    
    def test_prewarm_memory_fallback(self):
        """Test prewarm falls back to memory when Noopur unavailable"""
        router = CreatorRouter(self.memory_adapter)
        router.noopur = None  # No Noopur available
        
        # Store memory context
        for i in range(3):
            self.memory_adapter.store_interaction(
                self.test_user_id,
                {"topic": f"Memory Topic {i}", "module": "creator"},
                {"status": "success", "content": f"memory content {i}"}
            )
        
        input_data = {
            "topic": "New Topic",
            "goal": "Test Memory Fallback"
        }
        
        # Test prewarm
        result = router.prewarm_and_prepare("generate", self.test_user_id, input_data)
        
        # Should have memory context
        assert "related_context" in result
        assert isinstance(result["related_context"], list)
        assert len(result["related_context"]) <= 3
    
    def test_prewarm_missing_topic_goal(self):
        """Test prewarm with missing topic/goal data"""
        router = CreatorRouter(self.memory_adapter)
        
        # Mock Noopur
        router.noopur = Mock()
        
        input_data = {
            "type": "article"
            # Missing topic and goal
        }
        
        # Test prewarm
        result = router.prewarm_and_prepare("generate", self.test_user_id, input_data)
        
        # Should not call Noopur without topic/goal
        router.noopur.generate.assert_not_called()
        
        # Should return original data
        assert result["type"] == "article"
    
    def test_prewarm_nested_data_structure(self):
        """Test prewarm with nested data structure"""
        router = CreatorRouter(self.memory_adapter)
        
        # Mock Noopur
        mock_response = {
            "related_context": [{"text": "nested test", "score": 0.8}]
        }
        router.noopur = Mock()
        router.noopur.generate.return_value = mock_response
        
        input_data = {
            "data": {
                "topic": "Nested Topic",
                "goal": "Nested Goal",
                "type": "nested"
            }
        }
        
        # Test prewarm
        result = router.prewarm_and_prepare("generate", self.test_user_id, input_data)
        
        # Should extract from nested structure
        router.noopur.generate.assert_called_once()
        call_args = router.noopur.generate.call_args[0][0]
        assert call_args["topic"] == "Nested Topic"
        assert call_args["goal"] == "Nested Goal"
    
    def test_forward_feedback_success(self):
        """Test feedback forwarding with success"""
        router = CreatorRouter(self.memory_adapter)
        
        # Mock Noopur feedback response
        mock_response = {"status": "feedback_received", "id": 123}
        router.noopur = Mock()
        router.noopur.feedback.return_value = mock_response
        
        feedback_payload = {
            "generation_id": 456,
            "command": "+1"
        }
        
        # Test feedback forwarding
        result = router.forward_feedback(feedback_payload)
        
        # Verify feedback was forwarded
        router.noopur.feedback.assert_called_once_with(feedback_payload)
        assert result["status"] == "feedback_received"
        assert result["id"] == 123
    
    def test_forward_feedback_no_noopur(self):
        """Test feedback forwarding when Noopur unavailable"""
        router = CreatorRouter(self.memory_adapter)
        router.noopur = None
        
        feedback_payload = {
            "id": 789,
            "feedback": "positive"
        }
        
        # Test feedback forwarding
        result = router.forward_feedback(feedback_payload)
        
        # Should return disabled status
        assert result["status"] == "disabled"
    
    def test_forward_feedback_payload_normalization(self):
        """Test feedback payload normalization"""
        router = CreatorRouter(self.memory_adapter)
        
        # Mock Noopur
        router.noopur = Mock()
        router.noopur.feedback.return_value = {"status": "ok"}
        
        # Test different payload formats
        payloads = [
            {"id": 1, "feedback": "good"},
            {"generation_id": 2, "command": "+2"},
            {"custom_field": "custom_value"}
        ]
        
        for payload in payloads:
            result = router.forward_feedback(payload)
            
            # Should handle all payload formats
            router.noopur.feedback.assert_called()
            assert "status" in result or result.get("status") == "ok"
    
    def test_context_limit_enforcement(self):
        """Test context limits are enforced (3 for warm context)"""
        router = CreatorRouter(self.memory_adapter)
        
        # Store many interactions
        for i in range(10):
            self.memory_adapter.store_interaction(
                self.test_user_id,
                {"topic": f"Topic {i}", "module": "creator"},
                {"status": "success", "content": f"content {i}"}
            )
        
        input_data = {"topic": "New Topic", "goal": "Test Limits"}
        
        # Test prewarm (should use memory fallback)
        router.noopur = None
        result = router.prewarm_and_prepare("generate", self.test_user_id, input_data)
        
        # Should respect context limit
        if "related_context" in result:
            assert len(result["related_context"]) <= 3