# CreatorCore Backend Integration Notes for Aman

## Overview
The CreatorCore backend is now ready for integration with the CreatorCore Agent. This document explains how to call the APIs and what to expect in responses.

## Base URL
```
http://localhost:5000
```

## Key Integration Points

### 1. Content Generation with Context
**Endpoint:** `POST /generate`

**When to Call:**
- When the agent needs to generate new content (stories, ads, podcasts)
- Before generating, to get contextual information from past outputs

**Request Payload:**
```json
{
  "topic": "string - the main topic/subject",
  "goal": "string - what the content should achieve",
  "type": "string - 'story', 'ad', or 'podcast'"
}
```

**Response includes:**
- `related_context`: Array of up to 3 similar past generations
- Each context item has: `id`, `topic`, `output_text`, `similarity`, `feedback_score`, `combined_score`

**Integration Logic:**
```python
# Example integration code
response = requests.post("http://localhost:5000/generate", json={
    "topic": user_topic,
    "goal": user_goal,
    "type": content_type
})

if response.status_code == 200:
    data = response.json()
    context = data.get("related_context", [])

    # Use context to inform your generation
    if context:
        # Build context prompt from similar content
        context_text = "\n".join([item["output_text"] for item in context])
        # Include in your AI prompt
```

### 2. Feedback Submission
**Endpoint:** `POST /feedback`

**When to Call:**
- After showing generated content to user
- When user provides feedback (positive/negative comments)

**Request Payload:**
```json
{
  "id": "string - the generation ID from /generate response",
  "feedback": "string - user's feedback text"
}
```

**Scoring Logic:**
- Positive words ("good", "great", "love") → +0.5 score
- Negative words ("bad", "terrible", "hate") → -0.5 score
- Score affects future context retrieval (higher scored content gets priority)

### 3. History Retrieval
**Endpoint:** `GET /history/{topic}`

**When to Call:**
- To get the latest generation for a topic
- For continuity in conversations

## Expected Payloads

### From Agent to Backend
```json
// Generate request
{
  "topic": "Space Exploration",
  "goal": "Educate children about Mars",
  "type": "story"
}

// Feedback request
{
  "id": "507f1f77bcf86cd799439011",
  "feedback": "This is amazing work! I love the creativity."
}
```

### From Backend to Agent
```json
// Generate response
{
  "id": "507f1f77bcf86cd799439011",
  "topic": "Space Exploration",
  "output_text": "Generated story content...",
  "tokens_used": 150,
  "related_context": [
    {
      "id": "507f1f77bcf86cd799439012",
      "topic": "Space Exploration",
      "output_text": "Previous Mars story...",
      "similarity": 0.85,
      "feedback_score": 1.0,
      "combined_score": 0.935
    }
  ]
}
```

## Error Handling
- All endpoints return JSON with error messages
- Check `status_code` and handle 4xx/5xx appropriately
- Backend falls back to mock mode if database unavailable

## Testing
Run the smoke tests: `python backend/test_smoke.py`

## Deployment Notes
- Ensure sentence-transformers is installed
- MongoDB connection string via `MONGO_URI` env var
- Run migration script: `python migrate_db.py`

## Contact
For integration issues, refer to API_CONTRACT.md or DB_SCHEMA.md