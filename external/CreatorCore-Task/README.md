# CreatorCore Context Intelligence Backend

A Flask-based backend application for content generation with contextual memory and reinforced feedback. This project provides APIs for generating stories, ad scripts, and podcast scripts while maintaining context through embeddings and learning from user feedback.

## Features

- **Contextual Content Generation**: Generate stories, ad scripts, and podcast scripts with semantic similarity search
- **Vector Embeddings**: Store and retrieve related content using sentence-transformers embeddings
- **Reinforced Feedback Memory**: Score-based learning system that improves future generations
- **History Tracking**: Retrieve past generations for specific topics
- **Database Integration**: MongoDB for storing generations, embeddings, and feedback scores
- **Mock Mode**: Fallback to mock data when database is unavailable

## Installation

1. Clone the repository:
```bash
git clone https://github.com/noopurdhondsekar12/CreatorCore-Task.git
cd CreatorCore-Task
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
export MONGO_URI="your_mongodb_connection_string"
```

## Usage

### Running the Application

```bash
python backend/app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### Generate Content
```http
POST /generate
Content-Type: application/json

{
  "topic": "Your topic here",
  "goal": "Your goal here",
  "type": "story|ad|podcast"
}
```

#### Update Feedback
```http
POST /feedback
Content-Type: application/json

{
  "id": "generation_id",
  "feedback": "Your feedback here"
}
```

#### Get History
```http
GET /history/{topic}
```

## Context Intelligence Features

### Embeddings and Similarity Search
- Uses sentence-transformers (all-MiniLM-L6-v2) for generating 384-dimensional embeddings
- Cosine similarity search for finding related content
- Top-3 similar generations returned with each new generation

### Reinforced Feedback Learning
- Keyword-based scoring: positive words (+0.5), negative words (-0.5)
- Cumulative scores stored per generation
- Retrieval weighted by similarity + feedback score for improved context

### Migration and Backfill
- Run `python migrate_db.py` to backfill embeddings for existing data
- Automatic embedding generation for new generations

## Project Structure

```
CreatorCore-Task/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── db_utils.py         # Database utilities
│   ├── embeddings_utils.py # Embedding generation and similarity search
│   ├── prompts.py          # AI prompt templates
│   ├── test_smoke.py       # Smoke tests for all endpoints
│   ├── utils/
│   │   └── schema.json     # Data schema
│   ├── test_*.json         # Test data files
├── API_CONTRACT.md         # API documentation
├── DB_SCHEMA.md            # Database schema
├── INTEGRATION_NOTES.md    # Integration guide for Aman
├── FINAL_REFLECTION.md     # Project reflection
├── migrate_db.py           # Database migration script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Dependencies

- Flask: Web framework
- PyMongo: MongoDB driver
- LangChain Core: Prompt template management
- python-dotenv: Environment variable management
- sentence-transformers: Embedding generation
- numpy: Numerical computations for vectors

## Development

The application includes mock functions for testing without external dependencies. Set up a MongoDB instance for full functionality.

## License

This project is part of the CreatorCore Task.