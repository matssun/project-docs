# Import Rules and Standards

## Core Principle: Fail Fast on Missing Dependencies

All imports in this codebase **MUST** fail immediately if dependencies are not available. We reject the pattern of conditional/optional imports because they hide dependency issues and create runtime surprises.

## FORBIDDEN: Conditional Import Patterns

### ❌ NEVER Use Try/Except Around Imports
```python
# FORBIDDEN - Hides import failures
try:
    from some_library import SomeClass
    LIBRARY_AVAILABLE = True
except ImportError:
    # Mock or fallback implementation
    class SomeClass:
        pass
    LIBRARY_AVAILABLE = False
```

### ❌ NEVER Use ImportError/ModuleNotFoundError Handling
```python
# FORBIDDEN - Silent import failures
try:
    import optional_library
except ImportError:
    optional_library = None
```

### ❌ NEVER Use Optional Import Guards
```python
# FORBIDDEN - Runtime conditional behavior
HAS_REDIS = False
try:
    import redis
    HAS_REDIS = True
except ImportError:
    pass

def some_function():
    if HAS_REDIS:
        # Use redis
        pass
    else:
        # Fallback behavior
        pass
```

## REQUIRED: Direct Import Patterns

### ✅ Always Use Direct Imports
```python
# CORRECT - Import fails immediately if not available
from some_library import SomeClass
from another_module import required_function
import standard_library_module
```

### ✅ Declare All Dependencies Explicitly
- Add ALL required dependencies to `pyproject.toml` or `requirements.txt`
- No dependency should be "optional" in production code
- If a feature requires a library, declare it as required

### ✅ Use Proper Dependency Management
```toml
# pyproject.toml - CORRECT approach
[tool.poetry.dependencies]
python = "^3.13"
redis = "^6.4.0"           # Required, not optional
celery = "^5.5.0"          # Required, not optional
pydantic = "^2.11.0"       # Required, not optional
```

## Handling Different Environments

### For Development vs Production Dependencies
```toml
# Use dependency groups, not conditional imports
[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
mypy = "^1.0.0"

[tool.poetry.group.production.dependencies]
gunicorn = "^21.0.0"
```

### For Optional Features
Create separate packages or use dependency injection:

```python
# CORRECT - Dependency injection pattern
from abc import ABC, abstractmethod

class CacheStrategy(ABC):
    @abstractmethod
    def get(self, key: str) -> Any: ...

class RedisCacheStrategy(CacheStrategy):
    def __init__(self):
        import redis  # Import directly - fail if not available
        self.client = redis.Redis()

class MemoryCacheStrategy(CacheStrategy):
    def __init__(self):
        self.cache = {}

# Choose implementation via configuration, not import availability
def create_cache_strategy(strategy_type: str) -> CacheStrategy:
    if strategy_type == "redis":
        return RedisCacheStrategy()  # Will fail if Redis not installed
    else:
        return MemoryCacheStrategy()
```

## Testing Considerations

### ✅ Mock at Interface Boundaries in Tests
```python
# test_something.py - CORRECT
from unittest.mock import Mock, patch
import pytest

def test_redis_functionality():
    with patch('redis.Redis') as mock_redis:
        mock_redis.return_value.get.return_value = b'test_value'
        # Test your code here
```

### ❌ Never Mock Imports in Production Code
```python
# FORBIDDEN - Production code should never mock imports
try:
    import redis
except ImportError:
    # Creating mock in production code
    class redis:
        class Redis:
            pass
```

## Migration Guide for Existing Violations

### Step 1: Identify the Real Dependency
- What library is being conditionally imported?
- Is it truly optional or actually required?

### Step 2: Add to Dependencies
- Add the library to `pyproject.toml` or `requirements.txt`
- Update dependency versions if needed

### Step 3: Remove Conditional Logic
- Replace try/except with direct import
- Remove mock classes and fallback implementations
- Remove feature flags based on import availability

### Step 4: Update Architecture if Needed
- If truly optional, use dependency injection
- Create separate extension packages for optional features
- Use configuration-based feature toggles, not import-based

## Enforcement

### Automated Checks
- Add linting rules to detect try/except around imports
- Use `import` statement analysis in CI/CD
- Code review checklist includes import pattern verification

### Code Review Guidelines
- Reviewers MUST reject any PR with conditional imports
- Alternative solutions must be provided for any "optional" dependency needs
- Architecture discussions required for any new external dependencies

## Rationale

1. **Immediate Failure**: Dependencies should fail at startup, not during runtime
2. **Clear Requirements**: Dependencies should be explicit and visible
3. **Predictable Behavior**: Code behavior should not depend on import availability
4. **Easier Debugging**: Import failures are clearer than runtime feature gaps
5. **Better Testing**: Real dependencies enable proper integration testing
6. **Production Safety**: No surprises when dependencies are missing in production

## Examples of Proper Solutions

### Instead of Optional Redis:
```python
# Configuration-based approach
class CacheConfig:
    strategy: Literal["redis", "memory"] = "memory"
    redis_url: Optional[str] = None

def create_cache(config: CacheConfig) -> CacheStrategy:
    if config.strategy == "redis":
        if not config.redis_url:
            raise ValueError("Redis URL required for Redis strategy")
        import redis  # Direct import - fails if not available
        return RedisCacheStrategy(redis.from_url(config.redis_url))
    else:
        return MemoryCacheStrategy()
```

### Instead of Optional Monitoring:
```python
# Dependency injection approach
class MonitoringInterface(ABC):
    @abstractmethod
    def record_metric(self, name: str, value: float) -> None: ...

class PrometheusMonitoring(MonitoringInterface):
    def __init__(self):
        from prometheus_client import Counter  # Direct import
        self.counter = Counter('my_metric', 'Description')

class NoOpMonitoring(MonitoringInterface):
    def record_metric(self, name: str, value: float) -> None:
        pass  # No-op implementation

# Choose via configuration
monitoring = PrometheusMonitoring() if config.enable_monitoring else NoOpMonitoring()
```

This approach provides clear, predictable, and maintainable dependency management while ensuring immediate failure on missing dependencies.