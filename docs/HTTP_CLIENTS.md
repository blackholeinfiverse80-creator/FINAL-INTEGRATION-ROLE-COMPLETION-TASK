# HTTP Client Architecture

## Current HTTP Clients

### ResilientHTTPClient
**Location**: `src/utils/resilient_client.py`
**Purpose**: Robust HTTP communication with external services

**Features**:
- **Circuit Breaker**: Automatic failure detection and recovery
- **Retry Logic**: Exponential backoff with configurable attempts
- **Timeout Handling**: Configurable request timeouts
- **Session Management**: Persistent HTTP sessions

**Usage**:
```python
from src.utils.resilient_client import ResilientHTTPClient

client = ResilientHTTPClient("http://external-service:5002")
response = client.post("/generate", json={"prompt": "test"})
```

### NoopurClient  
**Location**: `src/utils/noopur_client.py`
**Purpose**: Specialized client for Noopur service integration

**Features**:
- **API Authentication**: Bearer token support
- **Noopur Operations**: generate, feedback, history
- **Error Handling**: Graceful fallback responses

**Usage**:
```python
from src.utils.noopur_client import NoopurClient

client = NoopurClient("http://noopur:5001", api_key="key")
result = client.generate({"topic": "AI", "goal": "tutorial"})
```

## Removed Components

### BridgeClient (Removed)
- **Reason**: Unused in codebase, redundant with ResilientHTTPClient
- **Alternative**: Use ResilientHTTPClient for external HTTP calls
- **Migration**: No migration needed - was not integrated

## Best Practices

1. **Use ResilientHTTPClient** for external service communication
2. **Use NoopurClient** for Noopur-specific operations  
3. **Configure timeouts** appropriately for your use case
4. **Handle circuit breaker states** in your application logic