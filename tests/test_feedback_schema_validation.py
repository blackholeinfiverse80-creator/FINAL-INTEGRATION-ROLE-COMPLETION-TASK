"""
Test feedback schema validation across Gateway, Storage, and Noopur forwarding
"""

import pytest
import sys
import os
from datetime import datetime
from pydantic import ValidationError

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.feedback_models import CanonicalFeedbackSchema
from src.core.gateway import Gateway

class TestFeedbackSchemaValidation:
    """Test canonical feedback schema validation"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test components"""
        self.gateway = Gateway()
    
    def test_valid_feedback_schema(self):
        """Test valid feedback passes validation"""
        valid_feedback = {
            "generation_id": 123,
            "command": "+2",
            "user_id": "test_user",
            "comment": "Excellent response"
        }
        
        # Should validate successfully
        schema = CanonicalFeedbackSchema(**valid_feedback)
        assert schema.generation_id == 123
        assert schema.command == "+2"
        assert schema.user_id == "test_user"
        assert schema.comment == "Excellent response"
        assert isinstance(schema.timestamp, datetime)
    
    def test_invalid_generation_id(self):
        """Test invalid generation_id rejection"""
        invalid_cases = [
            {"generation_id": 0, "command": "+1", "user_id": "user"},  # Zero
            {"generation_id": -1, "command": "+1", "user_id": "user"},  # Negative
            {"generation_id": "abc", "command": "+1", "user_id": "user"},  # String
        ]
        
        for case in invalid_cases:
            with pytest.raises(ValidationError):
                CanonicalFeedbackSchema(**case)
    
    def test_invalid_command(self):
        """Test invalid command rejection"""
        invalid_commands = ["+3", "-3", "0", "good", "bad", ""]
        
        for cmd in invalid_commands:
            with pytest.raises(ValidationError):
                CanonicalFeedbackSchema(
                    generation_id=123,
                    command=cmd,
                    user_id="user"
                )
    
    def test_invalid_user_id(self):
        """Test invalid user_id rejection"""
        invalid_cases = [
            {"generation_id": 123, "command": "+1", "user_id": ""},  # Empty
            {"generation_id": 123, "command": "+1"},  # Missing
        ]
        
        for case in invalid_cases:
            with pytest.raises(ValidationError):
                CanonicalFeedbackSchema(**case)
    
    def test_comment_length_validation(self):
        """Test comment length validation"""
        # Valid comment
        valid_comment = "A" * 500
        schema = CanonicalFeedbackSchema(
            generation_id=123,
            command="+1",
            user_id="user",
            comment=valid_comment
        )
        assert len(schema.comment) == 500
        
        # Invalid comment (too long)
        with pytest.raises(ValidationError):
            CanonicalFeedbackSchema(
                generation_id=123,
                command="+1",
                user_id="user",
                comment="A" * 501
            )
    
    def test_gateway_feedback_validation(self):
        """Test Gateway validates feedback using canonical schema"""
        # Valid feedback
        valid_data = {
            "generation_id": 456,
            "command": "-1",
            "user_id": "gateway_user",
            "comment": "Needs improvement"
        }
        
        validated = self.gateway.validate_feedback(valid_data)
        assert isinstance(validated, CanonicalFeedbackSchema)
        assert validated.generation_id == 456
        
        # Invalid feedback
        invalid_data = {
            "generation_id": -1,
            "command": "invalid",
            "user_id": ""
        }
        
        with pytest.raises(ValueError, match="Invalid feedback schema"):
            self.gateway.validate_feedback(invalid_data)
    
    def test_gateway_feedback_request_processing(self):
        """Test Gateway processes feedback requests with validation"""
        # Valid feedback request
        valid_request = {
            "generation_id": 789,
            "command": "+2",
            "user_id": "process_user"
        }
        
        response = self.gateway.process_request(
            module="creator",
            intent="feedback",
            user_id="process_user",
            data=valid_request
        )
        
        assert response["status"] == "success"
        assert "feedback_data" in response.get("result", {})
        
        # Invalid feedback request
        invalid_request = {
            "generation_id": "invalid",
            "command": "bad_command",
            "user_id": ""
        }
        
        response = self.gateway.process_request(
            module="creator",
            intent="feedback",
            user_id="process_user",
            data=invalid_request
        )
        
        assert response["status"] == "error"
        assert "Invalid feedback schema" in response["message"]
    
    def test_schema_format_conversions(self):
        """Test schema format conversions for storage and Noopur"""
        feedback = CanonicalFeedbackSchema(
            generation_id=999,
            command="-2",
            user_id="convert_user",
            comment="Test conversion"
        )
        
        # Storage format
        storage_format = feedback.to_storage_format()
        assert storage_format["generation_id"] == 999
        assert storage_format["command"] == "-2"
        assert storage_format["user_id"] == "convert_user"
        assert storage_format["comment"] == "Test conversion"
        assert "timestamp" in storage_format
        
        # Noopur format
        noopur_format = feedback.to_noopur_format()
        assert noopur_format["generation_id"] == 999
        assert noopur_format["command"] == "-2"
        assert noopur_format["user_id"] == "convert_user"
        assert noopur_format["comment"] == "Test conversion"
        assert "timestamp" not in noopur_format  # Excluded for Noopur
    
    def test_all_valid_commands(self):
        """Test all valid command values"""
        valid_commands = ["+2", "+1", "-1", "-2"]
        
        for cmd in valid_commands:
            schema = CanonicalFeedbackSchema(
                generation_id=100,
                command=cmd,
                user_id="cmd_user"
            )
            assert schema.command == cmd
    
    def test_timestamp_auto_generation(self):
        """Test timestamp is auto-generated when not provided"""
        before = datetime.utcnow()
        
        schema = CanonicalFeedbackSchema(
            generation_id=111,
            command="+1",
            user_id="time_user"
        )
        
        after = datetime.utcnow()
        
        assert before <= schema.timestamp <= after
    
    def test_optional_fields(self):
        """Test optional fields behavior"""
        # Minimal valid feedback
        minimal = CanonicalFeedbackSchema(
            generation_id=222,
            command="-1",
            user_id="minimal_user"
        )
        
        assert minimal.comment is None
        assert minimal.timestamp is not None
        
        # With optional fields
        with_optional = CanonicalFeedbackSchema(
            generation_id=333,
            command="+1",
            user_id="optional_user",
            comment="With comment",
            timestamp=datetime(2023, 1, 1, 12, 0, 0)
        )
        
        assert with_optional.comment == "With comment"
        assert with_optional.timestamp == datetime(2023, 1, 1, 12, 0, 0)