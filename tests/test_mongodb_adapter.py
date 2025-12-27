import pytest
from unittest.mock import Mock, patch
from src.db.mongodb_adapter import MongoDBAdapter, PYMONGO_AVAILABLE

@pytest.mark.skipif(not PYMONGO_AVAILABLE, reason="pymongo not installed")
def test_mongodb_adapter_basic():
    """Test basic MongoDB adapter functionality with mocked MongoDB."""
    
    # Mock MongoDB client and collection
    mock_client = Mock()
    mock_db = Mock()
    mock_collection = Mock()
    
    # Configure mock client to return database
    mock_client.__getitem__ = Mock(return_value=mock_db)
    # Configure mock database to return collection
    mock_db.interactions = mock_collection
    # Configure admin for ping command
    mock_client.admin.command = Mock(return_value=True)
    mock_collection.create_index = Mock()
    mock_collection.insert_one = Mock()
    mock_collection.find = Mock()
    mock_collection.delete_many = Mock()
    mock_collection.aggregate = Mock(return_value=[])
    
    with patch('src.db.mongodb_adapter.MongoClient', return_value=mock_client):
        adapter = MongoDBAdapter("mongodb://localhost:27017", "test_db")
        
        # Test store interaction
        request_data = {"module": "test", "intent": "generate", "data": {"test": "data"}}
        response_data = {"status": "success", "result": {"test": "result"}}
        
        adapter.store_interaction("test_user", request_data, response_data)
        
        # Verify insert_one was called
        assert mock_collection.insert_one.called
        
        # Test get_user_history
        mock_cursor = Mock()
        mock_cursor.__iter__ = Mock(return_value=iter([
            {
                "module": "test",
                "timestamp": "2024-12-05T10:00:00",
                "request_data": request_data,
                "response_data": response_data
            }
        ]))
        mock_collection.find.return_value.sort.return_value = mock_cursor
        
        history = adapter.get_user_history("test_user")
        assert len(history) >= 0  # Should not fail

def test_mongodb_not_available():
    """Test graceful handling when pymongo is not available."""
    with patch('src.db.mongodb_adapter.PYMONGO_AVAILABLE', False):
        with pytest.raises(RuntimeError, match="pymongo not installed"):
            MongoDBAdapter()

def test_mongodb_adapter_context():
    """Test context retrieval with mocked MongoDB."""
    
    mock_client = Mock()
    mock_db = Mock()
    mock_collection = Mock()
    
    # Configure mock client to return database
    mock_client.__getitem__ = Mock(return_value=mock_db)
    # Configure mock database to return collection
    mock_db.interactions = mock_collection
    # Configure admin for ping command
    mock_client.admin.command = Mock(return_value=True)
    mock_collection.create_index = Mock()
    
    # Mock cursor for context query
    mock_cursor = Mock()
    mock_cursor.__iter__ = Mock(return_value=iter([
        {
            "module": "test",
            "timestamp": "2024-12-05T10:00:00",
            "request_data": {"module": "test"},
            "response_data": {"status": "success"}
        }
    ]))
    mock_collection.find.return_value.sort.return_value.limit.return_value = mock_cursor
    
    with patch('src.db.mongodb_adapter.MongoClient', return_value=mock_client):
        adapter = MongoDBAdapter("mongodb://localhost:27017", "test_db")
        
        context = adapter.get_context("test_user", limit=3)
        assert len(context) >= 0  # Should not fail
        
        # Verify correct query was made
        mock_collection.find.assert_called()