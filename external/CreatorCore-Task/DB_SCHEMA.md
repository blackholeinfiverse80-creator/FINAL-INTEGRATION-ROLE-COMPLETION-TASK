# Database Schema

## Generation Table

| Field       | Type       | Description                          |
|-------------|------------|--------------------------------------|
| id          | INTEGER    | Primary key, auto-increment          |
| text        | TEXT       | The generated text content           |
| embedding   | JSON       | Vector embedding as list of floats   |
| score       | FLOAT      | Cumulative feedback score, default 0.0 |
| created_at  | DATETIME   | Timestamp of creation                |

### Notes
- Uses SQLite database (`context_intelligence.db`)
- Embedding is stored as JSON array of 384 floats (from all-MiniLM-L6-v2 model)
- Score is adjusted via feedback endpoint with commands like "+2" or "-1"