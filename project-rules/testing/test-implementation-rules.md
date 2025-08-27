# Test Implementation Rules & Conventions

## ⚠️ CRITICAL: Anti-Pattern Defense for Testing

**Claude is trained on suboptimal Python testing code from beginners. This codebase uses SUPERIOR testing architecture that explicitly rejects common testing anti-patterns.**

**Before implementing ANY test solution, check**: This document and the strategic framework.

**Key testing anti-patterns we reject:**
- ❌ Over-mocking → ✅ Testing Trophy with integration focus
- ❌ unittest.TestCase → ✅ pytest with fixtures
- ❌ Implementation-coupled tests → ✅ Behavior-focused tests
- ❌ Brittle assertion chains → ✅ Clear AAA pattern
- ❌ Scattered test setup → ✅ Centralized fixtures and shared patterns

## Foundational Testing Philosophy

### Risk-Based Testing Strategy

**🚨 CRITICAL RULE: Tests are risk management tools, not bug-finding exercises 🚨**

- **ALWAYS** prioritize tests based on business risk and criticality
- **ALWAYS** focus on validating requirements and mitigating critical risks
- **ALWAYS** design tests to actively make software fail in controlled environments
- **NEVER** pursue exhaustive coverage - focus on high-value, high-risk areas
- **NEVER** write tests just to increase coverage metrics

### Object-Oriented Testing Focus

**🚨 CRITICAL RULE: Test object interactions, not just isolated units 🚨**

- **ALWAYS** validate how objects communicate and collaborate
- **ALWAYS** test message passing between objects and components
- **ALWAYS** validate protocol adherence and interface contracts
- **NEVER** test implementation details - focus on observable behavior
- **NEVER** couple tests to internal private methods or attributes

## Testing Trophy Hierarchy (NON-NEGOTIABLE)

### Integration Tests: The Centerpiece

**🚨 CRITICAL RULE: Integration tests are the most valuable layer 🚨**

- **ALWAYS** prioritize integration tests that validate object interactions
- **ALWAYS** test component boundaries and message flow
- **ALWAYS** validate ServiceRegistry interactions and dependency injection
- **ALWAYS** test ValidationManager → ValidationProcess → ValidationOrchestrator flows
- **ALWAYS** test error handling integration through ValidationToErrorContextBridge
- **NEVER** skip integration tests in favor of isolated unit tests
- **NEVER** mock dependencies that are fast, deterministic, and easy to set up

### Unit Tests: Focused Foundation

- **ALWAYS** test individual components in isolation when integration is impractical
- **ALWAYS** use real objects when they are fast, deterministic, and easy to instantiate
- **ALWAYS** test protocol implementations and interface contracts
- **NEVER** mock everything - only mock when absolutely necessary

### Static Analysis: First Line of Defense

- **ALWAYS** run mypy type checking before any test execution
- **ALWAYS** use strict type checking configuration
- **ALWAYS** validate import structure and dependency compliance

### End-to-End Tests: Critical User Workflows Only

- **ALWAYS** limit to most critical, user-facing workflows
- **ALWAYS** test complete service interactions through real interfaces
- **NEVER** use E2E tests for unit-level functionality

## Framework & Tool Standards (NON-NEGOTIABLE)

### pytest: The Professional Standard

**🚨 CRITICAL RULE: ALL new tests MUST use pytest 🚨**

- **ALWAYS** use pytest for all new test development
- **ALWAYS** use pytest-mock for mocking (via `mocker` fixture)
- **ALWAYS** leverage pytest's fixture system for test setup
- **NEVER** use unittest.TestCase for new tests
- **NEVER** use unittest.mock directly - use pytest-mock

### Import Standards for Tests

**🚨 CRITICAL RULE: Test imports follow same rules as production code 🚨**

- **ALWAYS** use `from __future__ import annotations` for forward references
- **ALWAYS** use deep imports with full module paths
- **ALWAYS** import from `core_interfaces` for all protocol definitions
- **NEVER** use relative imports in test files
- **NEVER** use `TYPE_CHECKING` blocks in tests

## Test Structure Standards (NON-NEGOTIABLE)

### Arrange-Act-Assert (AAA) Pattern

**🚨 CRITICAL RULE: ALL tests MUST follow AAA pattern 🚨**

```python
def test_given_valid_data_when_validation_executed_then_result_is_successful():
    # ARRANGE: Set up test environment
    validation_manager = ValidationManager("test_context")
    validation_manager.add_rule(RequiredFieldRule("email"))
    test_data = {"email": "user@example.com"}
    
    # ACT: Execute the behavior under test
    result = validation_manager.validate(test_data)
    
    # ASSERT: Verify the outcome
    assert result.is_successful()
    assert len(result.issues) == 0
```

### Test Naming Conventions

**🚨 CRITICAL RULE: Test names MUST follow GIVEN-WHEN-THEN pattern 🚨**

- **ALWAYS** use descriptive, behavior-focused names
- **ALWAYS** follow pattern: `test_given_[condition]_when_[action]_then_[outcome]`
- **ALWAYS** use underscores to separate words for readability
- **NEVER** use generic names like `test_validation` or `test_login`

**Examples:**
```python
# ✅ GOOD: Descriptive, behavior-focused
def test_given_invalid_email_when_validation_executed_then_validation_error_raised()
def test_given_missing_required_field_when_data_validated_then_issues_contain_field_error()
def test_given_network_timeout_when_request_executed_then_timeout_error_reported()

# ❌ BAD: Generic, implementation-focused
def test_validate()
def test_error_handling()
def test_network_call()
```

### File and Directory Structure

**🚨 CRITICAL RULE: Follow modular test organization 🚨**

```
module_name/
├── tests/
│   ├── conftest.py              # Module-specific fixtures
│   ├── unit/                    # Unit tests
│   │   ├── test_component_a.py
│   │   └── test_component_b.py
│   └── integration/             # Integration tests
│       ├── test_manager_integration.py
│       └── test_service_integration.py
```

## Test Double Standards (NON-NEGOTIABLE)

### When to Use Each Test Double

**🚨 CRITICAL RULE: Use minimal test doubles - prefer real objects 🚨**

| Test Double | When to Use | Example Use Case |
|-------------|-------------|------------------|
| **Real Object** | Fast, deterministic, easy to set up | ValidationRule, ErrorContext, FieldPath |
| **Fake** | Complex state, need working substitute | InMemoryDatabase, FileSystemFake |
| **Stub** | Need controlled return values | External API responses, configuration values |
| **Mock** | Need to verify specific interactions | ServiceRegistry registration, event publication |
| **Dummy** | Fill required parameters | Unused dependencies in constructor |

### Mock Usage Guidelines

**🚨 CRITICAL RULE: Mock only when real objects are impractical 🚨**

**Use mocks for dependencies that are:**
- **Non-deterministic**: Current time, random numbers, sensor data
- **Slow**: Network I/O, database queries, file operations
- **External**: Third-party APIs, system services
- **Complex setup**: Requires extensive state configuration

**Use real objects for dependencies that are:**
- **Fast**: Validation rules, error contexts, data structures
- **Deterministic**: Pure functions, immutable objects
- **Simple**: Easy to construct and configure

### Mock Implementation Standards

```python
# ✅ GOOD: Using pytest-mock with specific interface
def test_given_network_error_when_request_executed_then_error_handled(mocker):
    # ARRANGE
    mock_client = mocker.Mock(spec=IHttpClient)
    mock_client.get.side_effect = ConnectionError("Network timeout")
    service = NetworkService(client=mock_client)
    
    # ACT
    result = service.fetch_data("test-url")
    
    # ASSERT
    assert result.is_error()
    mock_client.get.assert_called_once_with("test-url")

# ❌ BAD: Over-mocking with no spec
def test_network_service(mocker):
    mock_everything = mocker.Mock()
    # ... brittle test following
```

## Interface-Driven Test Architecture

### Protocol Testing Standards

**🚨 CRITICAL RULE: Test protocol implementations, not concrete classes 🚨**

```python
# ✅ GOOD: Testing protocol compliance
def test_given_validation_manager_when_validating_then_implements_ivalidation_manager():
    # ARRANGE
    manager = ValidationManager("test")
    
    # ACT & ASSERT: Verify protocol compliance
    assert isinstance(manager, IValidationManager)
    assert hasattr(manager, 'validate')
    assert hasattr(manager, 'add_rule')
    
    # Test protocol behavior
    result = manager.validate({})
    assert isinstance(result, IValidationResult)
```

### Service Registry Testing

**🚨 CRITICAL RULE: Test service registration and dependency injection 🚨**

```python
# ✅ GOOD: Integration test of service registry
def test_given_services_registered_when_dependency_requested_then_correct_service_returned():
    # ARRANGE
    registry = ServiceRegistry()
    validation_service = ValidationService()
    registry.register(IValidationService, validation_service)
    
    # ACT
    retrieved_service = registry.get(IValidationService)
    
    # ASSERT
    assert retrieved_service is validation_service
    assert isinstance(retrieved_service, IValidationService)
```

## Error Handling Test Standards

### Error Factory Testing

**🚨 CRITICAL RULE: Test error creation through factory patterns 🚨**

```python
# ✅ GOOD: Testing error factory
def test_given_validation_error_context_when_error_created_then_proper_error_returned():
    # ARRANGE
    error_factory = get_error_factory()
    error_context = ErrorContext(
        field_path=FieldPath("user.email"),
        error_code=ErrorCode.INVALID_VALUE,
        category=ErrorCategory.VALIDATION,
        severity=ErrorSeverity.ERROR,
        info_container=Mock(spec=IInfoContainer)
    )
    
    # ACT
    error = error_factory.create_validation_error(error_context)
    
    # ASSERT
    assert isinstance(error, IValidationError)
    assert error.error_code == ErrorCode.INVALID_VALUE
```

### ValidationToErrorContextBridge Testing

**🚨 CRITICAL RULE: Test validation-error integration through bridge 🚨**

```python
# ✅ GOOD: Testing bridge integration
def test_given_validation_context_when_converted_to_error_then_proper_error_context_created():
    # ARRANGE
    validation_context = ValidationContext("test")
    bridge = ValidationToErrorContextBridge()
    
    # ACT
    error_context = bridge.convert_to_error_context(validation_context)
    
    # ASSERT
    assert isinstance(error_context, IErrorContext)
    assert error_context.info_container is not None
```

## Fixture Standards

### Module-Specific Fixtures

**🚨 CRITICAL RULE: Use module-specific conftest.py for common fixtures 🚨**

```python
# conftest.py example
@pytest.fixture
def validation_manager():
    """Provide configured ValidationManager for tests."""
    manager = ValidationManager("test_context")
    return manager

@pytest.fixture
def error_factory():
    """Provide error factory for testing."""
    return get_error_factory()

@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton state between tests."""
    _reset_all_singletons()
    yield
    _reset_all_singletons()
```

### Shared Testing Framework Usage

**🚨 CRITICAL RULE: Use shared_testing module for common patterns 🚨**

```python
# ✅ GOOD: Using shared testing patterns
from shared_testing.framework.fixtures import create_test_context, create_test_state
from shared_testing.patterns.error_handling_patterns import ErrorHandlingPatterns

def test_error_factory_scenario():
    # ARRANGE
    scenario = ErrorHandlingPatterns.create_error_factory_scenario()
    context = create_test_context()
    
    # ACT & ASSERT based on shared pattern
```

## Test Data Management

### Test Data Standards

**🚨 CRITICAL RULE: Use typed, structured test data 🚨**

```python
# ✅ GOOD: Typed test data
@pytest.fixture
def sample_validation_data() -> Dict[str, Any]:
    return {
        "field_path": FieldPath("user.email"),
        "expected_type": "email",
        "actual_value": "test@example.com",
        "validation_rule": "email_format",
        "constraint": "must be valid email format"
    }

# ❌ BAD: Untyped, unclear test data
@pytest.fixture 
def test_data():
    return {"stuff": "things", "other": 123}
```

### Test Context Management

**🚨 CRITICAL RULE: Use proper test isolation and cleanup 🚨**

```python
# ✅ GOOD: Proper isolation with autouse fixture
@pytest.fixture(autouse=True)
def reset_test_state():
    """Reset all stateful components between tests."""
    _reset_all_singletons()
    yield
    _reset_all_singletons()
```

## Module-Specific Testing Rules

### Validation Module Testing

- **ALWAYS** test ValidationManager as the primary interface
- **ALWAYS** test validation rule composition and execution
- **ALWAYS** test XML schema validation with real XML documents
- **ALWAYS** test ValidationToErrorContextBridge integration
- **NEVER** test internal ValidationFactory directly
- **NEVER** bypass ValidationManager in tests

### Error Handling Module Testing

- **ALWAYS** test error factory patterns and error creation
- **ALWAYS** test strategy pattern implementation
- **ALWAYS** test interface-only architecture compliance
- **ALWAYS** use ErrorHandlingPatterns from shared_testing
- **NEVER** create ErrorRecord or Info objects in error handling tests
- **NEVER** test concrete error implementations directly

### Service Infrastructure Testing

- **ALWAYS** test ServiceRegistry registration and retrieval
- **ALWAYS** test dependency injection patterns
- **ALWAYS** validate service lifecycle management
- **NEVER** test services in isolation without registry context

## Assertion Standards

### Clear, Descriptive Assertions

**🚨 CRITICAL RULE: Assertions must be self-documenting 🚨**

```python
# ✅ GOOD: Clear, specific assertions
assert result.is_successful(), f"Validation failed: {result.issues}"
assert len(result.issues) == 1, f"Expected 1 issue, got {len(result.issues)}"
assert error.error_code == ErrorCode.INVALID_VALUE
assert isinstance(service, IValidationService)

# ❌ BAD: Unclear assertions
assert result
assert len(issues) > 0
assert error
```

### Protocol Compliance Testing

```python
# ✅ GOOD: Testing protocol compliance
def test_validation_manager_implements_protocol():
    manager = ValidationManager("test")
    assert isinstance(manager, IValidationManager)
    
    # Test all required protocol methods exist and work
    assert callable(getattr(manager, 'validate'))
    assert callable(getattr(manager, 'add_rule'))
```

## Testing Anti-Patterns (FORBIDDEN)

### ❌ Over-Mocking Anti-Pattern

```python
# ❌ FORBIDDEN: Over-mocking fast, simple objects
def test_validation_with_mocks(mocker):
    mock_field_path = mocker.Mock(spec=FieldPath)
    mock_rule = mocker.Mock(spec=IValidationRule)
    mock_context = mocker.Mock(spec=IValidationContext)
    # ... brittle test follows
```

```python
# ✅ CORRECT: Use real objects when practical
def test_validation_with_real_objects():
    # ARRANGE: Use real, fast objects
    field_path = FieldPath("user.email")
    rule = RequiredFieldRule("email")
    manager = ValidationManager("test")
    manager.add_rule(rule)
    
    # ACT & ASSERT
```

### ❌ Implementation Coupling Anti-Pattern

```python
# ❌ FORBIDDEN: Testing implementation details
def test_internal_method_calls(mocker):
    service = MyService()
    spy = mocker.spy(service, '_internal_helper_method')
    service.public_method()
    spy.assert_called_once()  # Brittle!
```

```python
# ✅ CORRECT: Testing observable behavior
def test_given_valid_input_when_service_called_then_expected_outcome():
    # ARRANGE
    service = MyService()
    
    # ACT
    result = service.public_method(valid_input)
    
    # ASSERT: Test observable outcome, not internal calls
    assert result.is_successful()
```

### ❌ Scattered Test Setup Anti-Pattern

```python
# ❌ FORBIDDEN: Repeated setup in every test
def test_validation_case_1():
    manager = ValidationManager("test")
    manager.add_rule(RequiredFieldRule("email"))
    # ... test logic

def test_validation_case_2():
    manager = ValidationManager("test")  # Repeated!
    manager.add_rule(RequiredFieldRule("email"))  # Repeated!
    # ... test logic
```

```python
# ✅ CORRECT: Centralized fixture setup
@pytest.fixture
def configured_validation_manager():
    manager = ValidationManager("test")
    manager.add_rule(RequiredFieldRule("email"))
    return manager

def test_validation_case_1(configured_validation_manager):
    # ACT & ASSERT using fixture
```

## Architecture Compliance Testing

### Interface Boundary Testing

**🚨 CRITICAL RULE: Test all module interface boundaries 🚨**

```python
# ✅ GOOD: Testing interface boundaries
def test_validation_to_error_bridge_maintains_interface_contract():
    # ARRANGE
    validation_context = ValidationContext("test")
    bridge = ValidationToErrorContextBridge()
    
    # ACT
    error_context = bridge.convert_to_error_context(validation_context)
    
    # ASSERT: Verify interface compliance
    assert isinstance(error_context, IErrorContext)
    assert isinstance(error_context.info_container, IInfoContainer)
```

### Service Registry Integration Testing

```python
# ✅ GOOD: Testing service registry patterns
def test_given_services_registered_when_validation_manager_created_then_dependencies_injected():
    # ARRANGE
    registry = ServiceRegistry()
    validation_service = ValidationService()
    registry.register(IValidationService, validation_service)
    
    # ACT
    manager = ValidationManager("test", service_registry=registry)
    
    # ASSERT
    assert manager._validation_service is validation_service
```

## Test Environment Standards

### Singleton Management

**🚨 CRITICAL RULE: Reset singleton state between tests 🚨**

```python
# ✅ REQUIRED: In conftest.py
@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests."""
    _reset_all_singletons()
    yield
    _reset_all_singletons()
```

### Test Isolation

**🚨 CRITICAL RULE: Each test must be completely isolated 🚨**

- **ALWAYS** reset all stateful components between tests
- **ALWAYS** use fresh instances for each test
- **ALWAYS** clean up side effects in teardown
- **NEVER** let tests depend on execution order
- **NEVER** share mutable state between tests

## Error Testing Patterns

### Error Factory Testing

```python
# ✅ GOOD: Testing error creation patterns
def test_given_validation_error_context_when_error_created_then_proper_type_returned():
    # ARRANGE
    factory = get_error_factory()
    context = ErrorContext(
        field_path=FieldPath("test.field"),
        error_code=ErrorCode.INVALID_VALUE,
        category=ErrorCategory.VALIDATION,
        severity=ErrorSeverity.ERROR,
        info_container=Mock(spec=IInfoContainer)
    )
    
    # ACT
    error = factory.create_validation_error(context)
    
    # ASSERT
    assert isinstance(error, IValidationError)
    assert error.field_path == FieldPath("test.field")
```

### Error Strategy Testing

```python
# ✅ GOOD: Testing error strategy patterns
def test_given_validation_error_when_strategy_applied_then_appropriate_handling():
    # ARRANGE
    error_context = create_validation_error_context()
    strategy = ValidationErrorStrategy()
    
    # ACT
    handled_error = strategy.handle_error(error_context)
    
    # ASSERT
    assert isinstance(handled_error, IValidationError)
    assert handled_error.category == ErrorCategory.VALIDATION
```

## Performance and Quality Standards

### Test Performance Requirements

- **Unit tests**: Must complete in < 100ms each
- **Integration tests**: Must complete in < 1s each
- **Test suite**: Must complete full run in < 30s

### Quality Metrics

- **Coverage**: Focus on critical paths, not metrics
- **Maintainability**: Tests should be easier to understand than production code
- **Reliability**: Zero flaky tests - fix or remove unreliable tests

## Continuous Integration Standards

### Pre-commit Requirements

**🚨 CRITICAL RULE: All tests must pass before commit 🚨**

```bash
# Required commands before commit:
poetry run mypy .          # Type checking
poetry run pytest         # All tests
```

### Test Categorization

```python
# Use pytest markers for test categorization
@pytest.mark.unit
def test_individual_component():
    pass

@pytest.mark.integration  
def test_component_interaction():
    pass

@pytest.mark.slow
def test_expensive_operation():
    pass
```

## Migration Strategy

### Existing Test Refactoring

**Phase 1**: All new tests use these rules immediately
**Phase 2**: Refactor most brittle existing tests (excessive mocks, unittest.TestCase)
**Phase 3**: Evaluate failing tests as refactoring opportunities

### Identifying Tests for Refactoring

**High Priority for Refactoring:**
- Tests with > 3 mocks
- Tests using unittest.TestCase
- Tests failing frequently due to implementation changes
- Tests with unclear names or purposes

## Final Reminder: Superior Architecture

**This codebase uses advanced testing patterns that are BETTER than common Python practices:**

- **Testing Trophy** > Test Pyramid
- **pytest fixtures** > unittest setup/teardown  
- **Interface-driven testing** > implementation testing
- **Risk-based testing** > coverage-driven testing
- **Integration focus** > unit test isolation obsession

**Remember**: Common Python testing != Good Python testing. Our patterns are superior.