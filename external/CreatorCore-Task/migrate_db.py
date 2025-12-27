#!/usr/bin/env python3
"""
Migration script for CreatorCore database.
Backfills embeddings for existing generations that don't have them.
Run this script after deploying the new embeddings functionality.
"""

import os
from pymongo import MongoClient
from embeddings_utils import generate_embedding, backfill_embeddings

def main():
    print("Starting CreatorCore database migration...")

    # Check MongoDB connection
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client["creatorcore"]
        client.admin.command('ping')
        print("✓ Connected to MongoDB")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("Running in mock mode - no actual migration performed")
        return

    # Run backfill
    print("Backfilling embeddings for existing generations...")
    backfill_embeddings()

    print("Migration completed successfully!")

if __name__ == "__main__":
    main()