# Sequence Flow Diagrams

## Generate Endpoint Flow
```
1. Client sends POST /generate with {"prompt": "user input"}
2. Backend simulates content generation: generated_text = prompt + " generated content."
3. Backend generates embedding using sentence-transformers model
4. Backend creates new Generation record with text, embedding, score=0.0
5. Backend commits to database
6. Backend retrieves all generations with embeddings
7. Backend computes cosine similarities and normalizes scores
8. Backend calculates ranking = 0.7 * similarity + 0.3 * normalized_score
9. Backend sorts by ranking descending, takes top 3
10. Backend returns {"generated_text": "...", "related_context": [...]}
```

## Feedback Endpoint Flow
```
1. Client sends POST /feedback with {"generation_id": 1, "command": "+2"}
2. Backend queries Generation by id
3. Backend validates generation exists
4. Backend parses command (e.g., "+2" -> +2.0)
5. Backend updates generation.score += adjustment
6. Backend commits changes to database
7. Backend returns {"message": "Feedback applied", "new_score": updated_score}
```

## History Endpoint Flow
```
1. Client sends GET /history
2. Backend queries all Generation records ordered by created_at DESC
3. Backend formats records as list of dicts
4. Backend returns JSON array of generations
```

## Migration Script Flow
```
1. Script initializes Flask app context
2. Script queries generations where embedding IS NULL
3. For each generation:
   a. Generate embedding from text
   b. Update generation.embedding
4. Script commits all changes
5. Script prints migration summary