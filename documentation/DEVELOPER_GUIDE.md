# Developer Guide - Core Integrator

## Module Development

### Quick Start

Create a new module in 3 steps:

#### 1. Create Module Structure
```
modules/
└── your_module/
    ├── __init__.py
    ├── config.json
    └── module.py
```

#### 2. Implement BaseModule

```python
# modules/your_module/module.py
from typing import Dict, Any, List
from modules.base import BaseModule

class YourModule(BaseModule):
    def process(self, data: Dict[str, Any], context: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process incoming data and return result dict."""
        # Your logic here
        result = {"output": "processed"}
        return result
    
    def metadata(self) -> Dict[str, Any]:
        """Optional: Return module metadata."""
        return {"name": "your_module", "version": "1.0.0"}
```

#### 3. Create config.json

```json
{
  "name": "your_module",
  "version": "1.0.0",
  "description": "Your module description",
  "author": "Your Name"
}
```

### Module Contract

**Required:**
- Inherit from `BaseModule`
- Implement `process(data, context)` method
- Return a plain dictionary (NOT CoreResponse)
- Include `config.json` with `name` and `version`

**The Gateway handles:**
- Response normalization to CoreResponse
- Context retrieval and injection
- Memory storage
- Error handling
- Logging

### Return Format

Your module should return:
```python
{
    "key": "value",
    "result": {...}
}
```

The Gateway wraps this into:
```python
{
    "status": "success",
    "message": "Module processed successfully",
    "result": {your_return_dict}
}
```

### Context Usage

Context provides the last 3 user interactions:
```python
def process(self, data: Dict[str, Any], context: List[Dict[str, Any]] = None):
    if context:
        previous_request = context[0]["request"]
        previous_response = context[0]["response"]
    # Use context for stateful processing
```

### Testing Your Module

```python
# tests/test_your_module.py
from modules.your_module.module import YourModule

def test_your_module():
    module = YourModule()
    result = module.process({"input": "test"}, context=[])
    assert "output" in result
```

### Module Registration

Modules are auto-discovered at startup. The loader:
1. Scans `modules/` directory
2. Validates `config.json`
3. Imports `module.py`
4. Finds BaseModule subclass
5. Registers with Gateway

### Error Handling

Return errors as plain dicts:
```python
if error_condition:
    return {"error": "Description of error"}
```

Gateway converts to:
```python
{
    "status": "error",
    "message": "Description of error",
    "result": {}
}
```

### Best Practices

1. **Keep it simple** - Modules should do one thing well
2. **Stateless** - Use context for state, not instance variables
3. **Fast** - Process requests quickly (< 5s)
4. **Validated** - Validate input data
5. **Documented** - Add docstrings and config metadata

## API Integration

### Making Requests

```bash
POST http://localhost:8001/core
Content-Type: application/json

{
  "module": "your_module",
  "intent": "generate",
  "user_id": "user123",
  "data": {
    "input": "your data"
  }
}
```

### Response Format

```json
{
  "status": "success",
  "message": "Module processed successfully",
  "result": {
    "your": "data"
  }
}
```

## Security (SSPL Phase III)

### Request Signing

Include headers:
```
X-SSPL-Signature: <base64_signature>
X-SSPL-Timestamp: <unix_timestamp>
X-SSPL-Nonce: <unique_nonce>
X-SSPL-Public-Key: <base64_public_key>
```

### Signature Generation

```python
import time
import base64
from nacl.signing import SigningKey

# Generate keypair
signing_key = SigningKey.generate()
verify_key = signing_key.verify_key

# Create payload
timestamp = str(int(time.time()))
nonce = "unique_nonce_123"
body = '{"module":"test","intent":"generate","user_id":"user1","data":{}}'

# Sign
message = f"{timestamp}:{nonce}:{body}".encode()
signature = signing_key.sign(message).signature

# Headers
headers = {
    "X-SSPL-Signature": base64.b64encode(signature).decode(),
    "X-SSPL-Timestamp": timestamp,
    "X-SSPL-Nonce": nonce,
    "X-SSPL-Public-Key": base64.b64encode(bytes(verify_key)).decode()
}
```

## Observability

### Health Check
```bash
GET /system/health
```

### Diagnostics
```bash
GET /system/diagnostics
```

### Logs
```bash
GET /system/logs/latest?limit=50
```

## Configuration

Environment variables:
```bash
DB_PATH=db/context.db
NOOPUR_BASE_URL=http://localhost:5001
INTEGRATOR_USE_NOOPUR=false
NOOPUR_API_KEY=your_key
```

## Troubleshooting

**Module not loading?**
- Check `config.json` has `name` and `version`
- Verify BaseModule inheritance
- Check logs in `logs/bridge/`

**Context not working?**
- Ensure `user_id` is provided
- Check memory with `GET /get-context?user_id=X`

**Security errors?**
- Verify signature generation
- Check timestamp is within 5 minutes
- Ensure nonce is unique

## Support

- API Docs: http://localhost:8001/docs
- Test Suite: `pytest tests/`
- Logs: `logs/bridge/`
