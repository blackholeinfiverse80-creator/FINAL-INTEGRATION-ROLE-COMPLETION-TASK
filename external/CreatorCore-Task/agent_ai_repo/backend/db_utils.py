import os
from pymongo import MongoClient
from datetime import datetime
import json

# MongoDB Atlas connection (placeholder - replace with actual URI after setup)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # Local fallback for testing
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Shorter timeout
    db = client["creatorcore"]
    # Test connection
    client.admin.command('ping')
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    print("Using mock mode for testing.")
    client = None
    db = None

# Collections
if db is not None:
    generations_collection = db["generations"]
    feedback_loops_collection = db["feedback_loops"]
else:
    generations_collection = None
    feedback_loops_collection = None

def insert_generation(data: dict):
    """
    Insert a new generation record into the generations collection.
    """
    if db is None:
        print("Mock insert:", data)
        return "mock_id_123"
    # Add timestamp if not provided
    if "timestamp" not in data:
        data["timestamp"] = datetime.utcnow().isoformat() + "Z"
    # Add iteration if not provided
    if "iteration" not in data:
        # Get the latest iteration for this topic
        latest = generations_collection.find_one({"topic": data["topic"]}, sort=[("iteration", -1)])
        data["iteration"] = str(int(latest["iteration"]) + 1) if latest else "1"
    result = generations_collection.insert_one(data)
    return str(result.inserted_id)

def get_latest(topic: str):
    """
    Get the latest generation for a given topic.
    """
    if db is None:
        return {"topic": topic, "output_text": "Mock latest output", "timestamp": "2023-10-01T12:00:00Z"}
    return generations_collection.find_one({"topic": topic}, sort=[("timestamp", -1)])

def update_feedback(id: str, feedback: str):
    """
    Update the feedback for a generation by its ID.
    """
    if db is None:
        print(f"Mock update feedback for {id}: {feedback}")
        return True
    from bson import ObjectId
    result = generations_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"feedback": feedback}}
    )
    return result.modified_count > 0

# Test functions with mock data
if __name__ == "__main__":
    # Mock data
    mock_data = {
        "topic": "Test Topic",
        "goal": "Test Goal",
        "output_text": "This is a test output.",
        "tokens_used": 50
    }

    # Test insert
    inserted_id = insert_generation(mock_data)
    print(f"Inserted ID: {inserted_id}")

    # Test get latest
    latest = get_latest("Test Topic")
    print(f"Latest generation: {latest}")

    # Test update feedback
    success = update_feedback(inserted_id, "Great work!")
    print(f"Feedback updated: {success}")