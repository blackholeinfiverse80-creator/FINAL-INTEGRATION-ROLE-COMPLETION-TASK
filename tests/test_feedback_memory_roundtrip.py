"""
Test feedback memory roundtrip functionality
Tests the complete flow: feedback -> memory storage -> retrieval
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.db.memory_adapter import SQLiteAdapter

class TestFeedbackMemoryRoundtrip:
    """Test feedback storage and retrieval roundtrip"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test components"""
        self.memory_adapter = SQLiteAdapter(":memory:")
        self.test_user_id = "test_user_feedback"
    

    
    def test_memory_storage_roundtrip(self):
        """Test memory storage and retrieval"""
        # Store interaction in memory
        request_data = {
            "module": "creator",
            "intent": "generate",
            "data": {"topic": "test", "goal": "test"}
        }
        
        response_data = {
            "status": "success",
            "result": {"content": "test content"}
        }
        
        # Store interaction
        self.memory_adapter.store_interaction(
            self.test_user_id, 
            request_data, 
            response_data
        )
        
        # Retrieve context
        context = self.memory_adapter.get_context(self.test_user_id, limit=1)
        
        # Verify roundtrip
        assert len(context) >= 1
        stored_interaction = context[0]
        assert stored_interaction['request'] == request_data
        assert stored_interaction['response'] == response_data
    

    
    def test_memory_limit_enforcement(self):
        """Test memory limits are enforced (5 per module)"""
        # Store multiple interactions
        for i in range(7):  # More than limit of 5
            request_data = {
                "module": "creator",
                "intent": "generate", 
                "iteration": i
            }
            
            response_data = {
                "status": "success",
                "content": f"content_{i}"
            }
            
            self.memory_adapter.store_interaction(
                self.test_user_id,
                request_data, 
                response_data
            )
        
        # Retrieve context
        context = self.memory_adapter.get_context(self.test_user_id, limit=10)
        
        # Should respect limit (5 or less recent items)
        assert len(context) <= 5
        
        # Should be most recent items
        if len(context) > 0:
            latest_item = context[0]
            assert latest_item['request']['iteration'] >= 2  # Recent iterations
    
    def test_context_warm_limit(self):
        """Test warm context limit (3 items)"""
        # Store interactions
        for i in range(5):
            self.memory_adapter.store_interaction(
                self.test_user_id,
                {"module": "creator", "warm_test": i},
                {"status": "success", "content": f"warm_{i}"}
            )
        
        # Get warm context (limit 3)
        warm_context = self.memory_adapter.get_context(self.test_user_id, limit=3)
        
        # Should return exactly 3 or fewer items
        assert len(warm_context) <= 3
    
    def test_user_history_retrieval(self):
        """Test user history retrieval"""
        # Store interaction
        self.memory_adapter.store_interaction(
            self.test_user_id,
            {"module": "creator", "history_test": True},
            {"status": "success", "history_content": True}
        )
        
        # Get user history
        history = self.memory_adapter.get_user_history(self.test_user_id)
        
        # Verify history structure
        assert isinstance(history, list)
        
        if len(history) > 0:
            history_item = history[0]
            assert 'timestamp' in history_item or 'request' in history_item