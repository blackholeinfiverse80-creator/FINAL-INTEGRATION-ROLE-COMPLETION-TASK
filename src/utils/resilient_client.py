import requests
import time
from typing import Dict, Any, Optional
from functools import wraps

class CircuitBreaker:
    """Simple circuit breaker for external service calls"""
    
    def __init__(self, failure_threshold: int = 3, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            
            raise e

def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 0.5):
    """Decorator for retry with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    wait_time = backoff_factor * (2 ** attempt)
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator

class ResilientHTTPClient:
    """HTTP client with retry and circuit breaker"""
    
    def __init__(self, base_url: str, circuit_breaker: Optional[CircuitBreaker] = None):
        self.base_url = base_url.rstrip('/')
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.session = requests.Session()
    
    @retry_with_backoff(max_retries=3)
    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Make HTTP request with timeout"""
        kwargs.setdefault('timeout', 5)
        response = self.session.request(method, f"{self.base_url}{endpoint}", **kwargs)
        response.raise_for_status()
        return response
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """POST request with circuit breaker"""
        try:
            response = self.circuit_breaker.call(self._make_request, "POST", endpoint, **kwargs)
            return response.json()
        except Exception:
            return {"error": "Service unavailable", "fallback": True}
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """GET request with circuit breaker"""
        try:
            response = self.circuit_breaker.call(self._make_request, "GET", endpoint, **kwargs)
            return response.json()
        except Exception:
            return {"error": "Service unavailable", "fallback": True}