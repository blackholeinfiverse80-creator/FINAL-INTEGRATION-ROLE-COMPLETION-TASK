try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    # If heavy dependencies aren't available, fall back to mock mode.
    print(f"Embedding model unavailable, running in mock mode: {e}")
    model = None
    import numpy as np

from pymongo import MongoClient
import os
from datetime import datetime

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["creatorcore"]
    client.admin.command('ping')
    generations_collection = db["generations"]
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    print("Using mock mode for embeddings.")
    client = None
    db = None
    generations_collection = None

def generate_embedding(text: str) -> list:
    """
    Generate embeddings for the given text.
    """
    if not text:
        return []
    if model is None:
        # Return a deterministic mock embedding for testing (small vector)
        vec = [float(len(text) % 10)] * 8
        return vec
    embedding = model.encode(text)
    return embedding.tolist()

def store_embedding(generation_id: str, embedding: list):
    """
    Store the embedding for a generation in the database.
    """
    if db is None:
        print(f"Mock store embedding for {generation_id}")
        return
    from bson import ObjectId
    generations_collection.update_one(
        {"_id": ObjectId(generation_id)},
        {"$set": {"embedding": embedding, "embedding_updated": datetime.utcnow().isoformat() + "Z"}}
    )

def cosine_similarity(vec1: list, vec2: list) -> float:
    """
    Calculate cosine similarity between two vectors.
    """
    if not vec1 or not vec2:
        return 0.0
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

def find_similar_generations(query_embedding: list, topic: str = None, top_k: int = 3, score_weight: float = 0.0):
    """
    Find top-k similar generations based on embeddings, optionally filtered by topic.
    Incorporates feedback score weighting.
    """
    if db is None:
        return [{"topic": "Mock Topic", "output_text": "Mock similar content", "similarity": 0.8}]

    # Build query
    query = {"embedding": {"$exists": True}}
    if topic:
        query["topic"] = topic

    # Get all matching documents
    docs = list(generations_collection.find(query))

    similarities = []
    for doc in docs:
        if "embedding" in doc:
            sim = cosine_similarity(query_embedding, doc["embedding"])
            score = doc.get("feedback_score", 0.0)
            # Combine similarity and score (weighted)
            combined_score = sim + (score * score_weight)
            similarities.append({
                "id": str(doc["_id"]),
                "topic": doc.get("topic", ""),
                "output_text": doc.get("output_text", ""),
                "similarity": sim,
                "feedback_score": score,
                "combined_score": combined_score
            })

    # Sort by combined score and return top-k
    similarities.sort(key=lambda x: x["combined_score"], reverse=True)
    return similarities[:top_k]

def backfill_embeddings():
    """
    Backfill embeddings for existing generations that don't have them.
    """
    if db is None:
        print("Mock backfill embeddings")
        return

    docs = generations_collection.find({"embedding": {"$exists": False}})
    count = 0
    for doc in docs:
        text = doc.get("output_text", "")
        if text:
            embedding = generate_embedding(text)
            store_embedding(str(doc["_id"]), embedding)
            count += 1
    print(f"Backfilled embeddings for {count} generations")

if __name__ == "__main__":
    # Test embedding generation
    test_text = "This is a test generation output."
    embedding = generate_embedding(test_text)
    print(f"Embedding dimension: {len(embedding)}")

    # Test similarity
    emb1 = generate_embedding("Hello world")
    emb2 = generate_embedding("Hello universe")
    sim = cosine_similarity(emb1, emb2)
    print(f"Similarity: {sim}")

    # Backfill if connected
    backfill_embeddings()