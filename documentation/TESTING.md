# Testing Guide - Core Integrator

## Overview
Comprehensive testing guide for the Core Integrator system including memory chain tests, module tests, security tests, and MongoDB integration tests.

## Quick Start

### Setup Testing Environment
```bash
# Install test dependencies
pip install pytest httpx

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_memory_chain.py -v
```

## Memory Chain Testing

### Test Memory Limit (5 entries per user/module)
```python
# tests/test_memory_chain.py
def test_memory_chain_limit():
    """Test that memory stores only 5 entries per user per module"""
    # Creates 6 interactions, verifies only 5 remain
    # Tests deterministic retention (newest first)
```

### Cross-Module Isolation Test
```python
def test_cross_module_isolation():
    """Test that different modules maintain separate 5-entry limits"""
    # Verifies finance and education modules don't interfere
```

## Module Testing

### BaseModule Contract Test
```python
# tests/test_module_exec.py
def test_module_returns_proper_core_response():
    """Test that module returns proper CoreResponse format"""
    # Verifies status, message, result structure
```

### Module Loader Test
```python
# tests/test_module_loader.py
def test_loader_finds_sample_text():
    """Test dynamic module loading"""
    # Verifies sample_text module loads correctly
    # Checks error handling for invalid modules
```

## Security Testing

### SSPL Middleware Test
```python
# tests/test_sspl_middleware.py
def test_middleware_allows_when_pynacl_missing():
    """Test graceful degradation when PyNaCl unavailable"""

def test_middleware_rejects_stale_timestamp():
    """Test timestamp freshness validation"""

def test_middleware_replays_are_blocked():
    """Test nonce anti-replay protection"""
```

### Signature Verification Test
```python
# tests/test_sspl_signature.py
def test_signature_verification_and_middleware():
    """Test Ed25519 signature verification"""
    # Uses real PyNaCl signing for full verification
```

## MongoDB Testing

### Adapter Test
```python
# tests/test_mongodb_adapter.py
def test_mongodb_adapter_basic():
    """Test MongoDB adapter with mocked MongoDB"""
    # Tests store_interaction, get_user_history, get_context
```

### Live MongoDB Test
```bash
# Requires MongoDB server running
python -c "
from src.db.mongodb_adapter import MongoDBAdapter
adapter = MongoDBAdapter()
adapter.store_interaction('test_user', 
    {'module': 'test', 'data': {}}, 
    {'status': 'success'})
print('MongoDB test successful')
"
```

## Integration Testing

### Creator Pipeline Test
```python
# tests/test_creator_pipeline.py
def test_creator_prewarm_and_invoke():
    """Test creator agent with context pre-warming"""
    # Mocks Noopur integration
    # Tests full creator workflow
```

### Gateway Integration Test
```python
# Test full request flow through gateway
response = gateway.process_request(
    module="sample_text",
    intent="generate", 
    user_id="test_user",
    data={"input_text": "Hello world"}
)
assert response["status"] == "success"
```

## API Testing with Postman

### Collection Import
1. Import `postman_collection.json`
2. Set environment variables:
   - `base_url`: http://localhost:8001
   - `user_id`: test_user_123

### Key Test Cases
- **Core Endpoint**: POST `/core`
- **Get History**: GET `/get-history?user_id=test_user`
- **Get Context**: GET `/get-context?user_id=test_user`
- **Health Check**: GET `/system/health`
- **Diagnostics**: GET `/system/diagnostics`

## Performance Testing

### Memory Performance
```python
# Test memory operations under load
import time
start = time.time()
for i in range(1000):
    memory.store_interaction(f"user_{i}", request_data, response_data)
print(f"1000 interactions stored in {time.time() - start:.2f}s")
```

### Concurrent Access Test
```python
import threading
import concurrent.futures

def store_interactions(user_id, count):
    for i in range(count):
        memory.store_interaction(user_id, request_data, response_data)

# Test concurrent writes
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(store_interactions, f"user_{i}", 100) 
               for i in range(10)]
    concurrent.futures.wait(futures)
```

## Test Data Management

### Test Database Setup
```python
# Use in-memory database for tests
memory = ContextMemory(":memory:")

# Or temporary file
import tempfile
with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
    memory = ContextMemory(tmp.name)
```

### Cleanup After Tests
```python
def cleanup_test_data():
    """Remove test data from database"""
    # Tests should use isolated databases
    # Production database should not be affected
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/ -v
```

## Test Coverage

### Generate Coverage Report
```bash
pip install pytest-cov
python -m pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html
```

### Target Coverage
- **Core modules**: >90%
- **Agents**: >85%
- **Database adapters**: >95%
- **Security components**: >95%

## Debugging Tests

### Verbose Output
```bash
python -m pytest tests/ -v -s
```

### Debug Specific Test
```bash
python -m pytest tests/test_memory_chain.py::test_memory_chain_limit -v -s
```

### Logging in Tests
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Test Environment Variables

### Required for Testing
```bash
# .env.test
DB_PATH=:memory:
SSPL_ENABLED=false
INTEGRATOR_USE_NOOPUR=false
USE_MONGODB=false
```

### Load Test Environment
```python
import os
os.environ.update({
    'DB_PATH': ':memory:',
    'SSPL_ENABLED': 'false'
})
```

## Known Test Issues

### Windows-Specific
- Database file locking may prevent cleanup
- Use `del memory` before file deletion
- Some tests may need `pytest-xdist` for parallel execution

### MongoDB Tests
- Require MongoDB server running
- Use `@pytest.mark.skipif` for conditional tests
- Mock MongoDB client for unit tests

## Test Maintenance

### Adding New Tests
1. Create test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Use descriptive test function names
4. Include docstrings explaining test purpose
5. Add to CI pipeline if needed

### Test Review Checklist
- [ ] Tests are isolated (no shared state)
- [ ] Tests clean up after themselves
- [ ] Tests have clear assertions
- [ ] Tests cover both success and error cases
- [ ] Tests are deterministic (no random failures)

## Support

For testing issues:
1. Check test logs for specific error messages
2. Verify test environment setup
3. Ensure all dependencies are installed
4. Check database permissions and paths
5. Review test isolation and cleanup