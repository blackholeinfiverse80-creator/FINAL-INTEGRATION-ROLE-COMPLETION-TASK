# Core Integrator Demo Script

## Pre-Demo Setup (5 minutes)

1. **Start the server:**
   ```bash
   cd c:\Aman\Core-Integrator-Sprint-1.1-
   python main.py
   ```

2. **Verify health:**
   ```bash
   curl http://localhost:8001/system/health
   ```

3. **Open Postman/Browser:**
   - API Docs: http://localhost:8001/docs

## Demo Flow (10 minutes)

### 1. System Overview (2 min)

**Show:** Architecture diagram
**Say:** "Core Integrator is a Sovereign-aligned orchestration platform that routes requests to specialized agents with built-in memory, security, and observability."

**Key Points:**
- Dynamic module loading
- Context-aware processing
- SSPL Phase III security
- Cross-agent routing

### 2. Health & Diagnostics (1 min)

**Request:**
```bash
GET http://localhost:8001/system/health
```

**Show:** Healthy status, database connectivity, loaded modules

**Request:**
```bash
GET http://localhost:8001/system/diagnostics
```

**Show:** Module registry, memory stats, security status

### 3. Basic Module Request (2 min)

**Request:**
```bash
POST http://localhost:8001/core
Content-Type: application/json

{
  "module": "sample_text",
  "intent": "generate",
  "user_id": "demo_user",
  "data": {
    "text": "Hello CreatorCore team! This is a demonstration of the Core Integrator."
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Text processed successfully",
  "result": {
    "word_count": 11,
    "char_count": 72,
    "processed_text": "Hello CreatorCore team! This is a demonstration of the Core Integrator."
  }
}
```

**Say:** "Notice the normalized response format - all modules return consistent CoreResponse structure."

### 4. Context Memory Demo (2 min)

**Request 1:**
```bash
POST http://localhost:8001/core

{
  "module": "finance",
  "intent": "generate",
  "user_id": "demo_user",
  "data": {
    "report_type": "quarterly",
    "period": "Q4 2024"
  }
}
```

**Request 2:**
```bash
POST http://localhost:8001/core

{
  "module": "finance",
  "intent": "analyze",
  "user_id": "demo_user",
  "data": {
    "metric": "revenue"
  }
}
```

**Show Context:**
```bash
GET http://localhost:8001/get-context?user_id=demo_user
```

**Say:** "The system maintains last 3 interactions per user, providing context for stateful processing. Each module maintains separate 5-entry limits."

### 5. Module Isolation (1 min)

**Request:**
```bash
POST http://localhost:8001/core

{
  "module": "education",
  "intent": "generate",
  "user_id": "demo_user",
  "data": {
    "topic": "Python basics"
  }
}
```

**Show History:**
```bash
GET http://localhost:8001/get-history?user_id=demo_user
```

**Say:** "Notice finance and education modules maintain separate memory chains - cross-module isolation ensures clean context."

### 6. Security Layer (1 min)

**Show:** SSPL middleware code
**Say:** "Every request is validated with Ed25519 signatures, timestamp checks, and nonce-based replay protection."

**Key Features:**
- Signature verification
- 5-minute timestamp window
- Nonce store prevents replay attacks
- Audit chain logging

### 7. Dynamic Module Loading (1 min)

**Show:** `modules/` directory structure
**Say:** "New modules are auto-discovered at startup. Just drop in a folder with config.json and module.py."

**Show Diagnostics:**
```bash
GET http://localhost:8001/system/diagnostics
```

**Point out:** Loaded modules list

## Demo Talking Points

### Architecture Strengths
- **Modular:** Easy to add new agents/modules
- **Secure:** SSPL Phase III compliance
- **Observable:** Health, diagnostics, logs
- **Deterministic:** Predictable memory retention
- **Interoperable:** Noopur backend integration ready

### Technical Highlights
- BaseModule contract enforcement
- Automatic response normalization
- Context-aware processing
- Cross-agent routing
- Memory adapter pattern (SQLite ↔ MongoDB)

### Production Ready
- ✅ Full test coverage
- ✅ Structured logging
- ✅ Error handling
- ✅ API documentation
- ✅ Security middleware
- ✅ Health monitoring

## Q&A Preparation

**Q: How do I add a new module?**
A: Create folder in `modules/`, add config.json and module.py implementing BaseModule. Auto-discovered on restart.

**Q: How does security work?**
A: Ed25519 signature verification with timestamp and nonce validation. See DEVELOPER_GUIDE.md for implementation.

**Q: Can it scale?**
A: Yes - memory adapter pattern allows switching from SQLite to MongoDB/Redis. Stateless design enables horizontal scaling.

**Q: Integration with Noopur?**
A: Built-in via NoopurClient and RemoteNoopurAdapter. Toggle with INTEGRATOR_USE_NOOPUR env var.

**Q: What about error handling?**
A: Gateway normalizes all responses. Modules return plain dicts, gateway wraps in CoreResponse with proper status codes.

## Post-Demo

**Show:**
- Test suite: `pytest tests/`
- Documentation: README.md, DEVELOPER_GUIDE.md
- Logs: `logs/bridge/`
- Postman collection: `postman_collection.json`

**Next Steps:**
- Deploy to staging
- Integrate remaining CreatorCore modules
- Enable Noopur backend connection
- Production security hardening
