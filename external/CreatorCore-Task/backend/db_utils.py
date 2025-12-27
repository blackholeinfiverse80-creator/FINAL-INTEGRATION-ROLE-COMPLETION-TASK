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
    doc = generations_collection.find_one({"topic": topic}, sort=[("timestamp", -1)])
    if doc:
        # Convert ObjectId to string for JSON serialization
        doc["_id"] = str(doc["_id"])
    return doc

def update_feedback(id: str, feedback: str):
    """
    Update the feedback for a generation by its ID and calculate feedback score.
    """
    if db is None:
        print(f"Mock update feedback for {id}: {feedback}")
        return True

    # Scoring logic: positive keywords increase score, negative decrease
    positive_keywords = ["good", "great", "excellent", "amazing", "love", "like", "perfect", "awesome"]
    negative_keywords = ["bad", "terrible", "awful", "hate", "dislike", "poor", "worst", "horrible"]

    feedback_lower = feedback.lower()
    score_change = 0

    for word in positive_keywords:
        if word in feedback_lower:
            score_change += 0.5

    for word in negative_keywords:
        if word in feedback_lower:
            score_change -= 0.5

    from bson import ObjectId
    # Get current score
    doc = generations_collection.find_one({"_id": ObjectId(id)})
    current_score = doc.get("feedback_score", 0.0) if doc else 0.0

    new_score = current_score + score_change

    result = generations_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"feedback": feedback, "feedback_score": new_score}}
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