# API Endpoints Reference

Base URL: `http://localhost:8001`

## 1. POST /core
**Main gateway endpoint for processing agent requests**

### Input:
```json
{
  "module": "finance|education|creator|sample_text",
  "intent": "generate|analyze|review", 
  "user_id": "string (min_length=1)",
  "data": {
    // Module-specific data (optional)
  }
}
```

### Examples:

#### Finance Module:
```json
{
  "module": "finance",
  "intent": "generate",
  "user_id": "12345",
  "data": {
    "report_type": "quarterly"
  }
}
```

#### Education Module:
```json
{
  "module": "education", 
  "intent": "generate",
  "user_id": "student123",
  "data": {
    "subject": "mathematics",
    "level": "beginner"
  }
}
```

#### Creator Module:
```json
{
  "module": "creator",
  "intent": "generate", 
  "user_id": "creator456",
  "data": {
    "topic": "AI Technology",
    "goal": "Educational content",
    "type": "story"
  }
}
```

#### Sample Text Module:
```json
{
  "module": "sample_text",
  "intent": "generate",
  "user_id": "test_user",
  "data": {
    "input_text": "Hello world this is a test"
  }
}
```

### Output:
```json
{
  "status": "success|error",
  "message": "string",
  "result": {
    // Module-specific result data
  }
}
```

---

## 2. POST /feedback
**Submit feedback for generated content**

### Input:
```json
{
  "generation_id": 1,
  "command": "+2|+1|-1|-2",
  "user_id": "string (min_length=1)",
  "comment": "string (max_length=500, optional)"
}
```

### Example:
```json
{
  "generation_id": 1,
  "command": "+1", 
  "user_id": "test_user",
  "comment": "Great work!"
}
```

### Output:
```json
{
  "status": "success|error",
  "message": "string",
  "result": {}
}
```

---

## 3. GET /get-history
**Get full interaction history for a user**

### Input (Query Parameter):
- `user_id`: string (required)

### Example:
```
GET /get-history?user_id=12345
```

### Output:
```json
[
  {
    "module": "finance",
    "timestamp": "2024-01-01T12:00:00",
    "request": {
      "module": "finance",
      "intent": "generate", 
      "user_id": "12345",
      "data": {"report_type": "quarterly"}
    },
    "response": {
      "status": "success",
      "message": "Financial report generated",
      "result": {...}
    }
  }
]
```

---

## 4. GET /get-context
**Get recent context (last 3 interactions) for a user**

### Input (Query Parameter):
- `user_id`: string (required)

### Example:
```
GET /get-context?user_id=12345
```

### Output:
```json
[
  {
    "module": "finance",
    "timestamp": "2024-01-01T12:00:00", 
    "request": {...},
    "response": {...}
  }
]
```

---

## 5. GET /
**Root endpoint with API information**

### Input: None

### Output:
```json
{
  "message": "Unified Backend Bridge API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## 6. GET /system/health
**System health check**

### Input: None

### Output:
```json
{
  "status": "healthy|degraded",
  "components": {
    "database": "healthy|unhealthy: error",
    "mongodb": "healthy|unhealthy: error",
    "external_service": "healthy|unhealthy: error",
    "gateway": "healthy",
    "modules": 4
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "insightflow_event": {...}
}
```

---

## 7. GET /system/diagnostics
**System diagnostics with module load status**

### Input: None

### Output:
```json
{
  "module_load_status": {
    "finance": "valid|invalid",
    "education": "valid|invalid", 
    "creator": "valid|invalid",
    "sample_text": "valid|invalid"
  },
  "integration_ready": true,
  "integration_checks": {
    "core_modules_loaded": true,
    "database_accessible": true,
    "gateway_initialized": true,
    "memory_adapter_ready": true
  },
  "integration_score": 1.0,
  "readiness_reason": "all_checks_passed",
  "failing_components": [],
  "timestamp": "2024-01-01T12:00:00Z",
  "modules": {
    "finance": "FinanceAgent",
    "education": "EducationAgent",
    "creator": "CreatorAgent"
  },
  "memory": {
    "total_interactions": 0,
    "unique_users": 0,
    "db_path": "data/context.db",
    "adapter_type": "SQLiteAdapter"
  },
  "security": {
    "nonce_store_enabled": false,
    "sspl_middleware": false
  },
  "version": "1.0.0"
}
```

---

## 8. GET /creator/history
**Get creator generation history**

### Input (Query Parameter):
- `user_id`: string (optional, default="all")

### Example:
```
GET /creator/history?user_id=creator456
```

### Output:
```json
{
  "status": "success|error",
  "message": "string", 
  "result": [...]
}
```

---

## 9. GET /system/logs/latest
**Get latest log entries**

### Input (Query Parameter):
- `limit`: integer (optional, default=50)

### Example:
```
GET /system/logs/latest?limit=100
```

### Output:
```json
{
  "log_file": "logs/bridge/app.log",
  "entries": [
    "2024-01-01 12:00:00 - INFO - Request processed",
    "2024-01-01 12:00:01 - ERROR - Database error"
  ],
  "count": 2
}
```

---

## Common Error Responses

### 422 Validation Error:
```json
{
  "detail": "Response validation error: Invalid module name"
}
```

### 500 Internal Server Error:
```json
{
  "detail": "Agent processing failed: Database connection error"
}
```

---

## Module-Specific Data Formats

### Finance Module Data:
```json
{
  "report_type": "quarterly|annual|monthly",
  "department": "string",
  "metrics": ["revenue", "expenses"]
}
```

### Education Module Data:
```json
{
  "subject": "mathematics|science|history",
  "level": "beginner|intermediate|advanced",
  "topic": "string"
}
```

### Creator Module Data:
```json
{
  "topic": "string",
  "goal": "string", 
  "type": "story|article|blog|social",
  "length": "short|medium|long"
}
```

### Sample Text Module Data:
```json
{
  "input_text": "string"
}
```