# API Contract

## Endpoints

### POST /generate
Generates content based on prompt, stores it with embedding, and returns related context.

**Request Format:**
```json
{
  "prompt": "string"
}
```

**Response Format:**
```json
{
  "generated_text": "string",
  "related_context": [
    {
      "text": "string",
      "score": 0.85
    }
  ]
}
```

**Example:**
Request:
```json
{
  "prompt": "Write a story about AI"
}
```
Response:
```json
{
  "generated_text": "Write a story about AI generated content.",
  "related_context": [
    {
      "text": "Previous generation text",
      "score": 0.83
    }
  ]
}
```

### POST /feedback
Applies feedback to adjust the score of a generation.

**Request Format:**
```json
{
  "generation_id": 1,
  "command": "+2"
}
```

**Response Format:**
```json
{
  "message": "Feedback applied",
  "new_score": 2.0
}
```

**Example:**
Request:
```json
{
  "generation_id": 1,
  "command": "-1"
}
```
Response:
```json
{
  "message": "Feedback applied",
  "new_score": -1.0
}
```

### GET /history
Retrieves the history of all generations.

**Request Format:**
None (GET request)

**Response Format:**
```json
[
  {
    "id": 1,
    "text": "Generated text",
    "score": 0.0,
    "created_at": "2023-11-11T10:00:00"
  }
]
```

**Example:**
Response:
```json
[
  {
    "id": 1,
    "text": "Sample text",
    "score": 2.0,
    "created_at": "2023-11-11T10:00:00"
  }
]
```

## Integration Notes
- All requests/responses are JSON
- Embeddings use sentence-transformers all-MiniLM-L6-v2
- Related context ranking formula: 0.7 * cosine_similarity + 0.3 * normalized_feedback_score
- Score normalization: (score - min_score) / (max_score - min_score) across all generations
- Scores are cumulative and adjusted by feedback commands (+2, -1, etc.)