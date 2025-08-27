# AI Agent Implementation: Testing Strategy & Standards

## Overview

This document provides the essential testing strategy for the AI agent governance system implementation. It consolidates our professional testing standards into actionable guidelines for achieving high-quality, maintainable, and reliable test coverage.

---

## 🏆 TESTING PHILOSOPHY

### Core Principle: Risk-Based Testing

Testing is **not** about finding all bugs (impossible) but about **identifying and mitigating business risks**. Focus testing efforts on:

1. **Critical Functionality**: Agent orchestration, contract validation, LTL verification
2. **Integration Points**: Agent communication, system boundaries  
3. **Error Conditions**: Failure scenarios, edge cases, recovery mechanisms
4. **Performance Requirements**: Response times, throughput, scalability

### Testing Trophy Hierarchy

We follow the **Testing Trophy** model, not the traditional Test Pyramid:

```
        🏆 E2E Tests
       (Critical workflows only)
         
    🔗 Integration Tests ⭐
   (Primary focus - object interactions)
   
  🧪 Unit Tests + 📊 Static Analysis
 (Foundation - fast feedback loops)
```

**Priority Order:**
1. **Integration Tests** - Validate agent interactions and workflows
2. **Unit Tests** - Validate individual components in isolation
3. **Static Analysis** - Catch issues before runtime (mypy, linting)
4. **E2E Tests** - Critical user scenarios only (minimal, focused)

---

## 🧰 TESTING TOOLS & FRAMEWORK

### Required Testing Stack

```toml
# pyproject.toml - Testing dependencies
[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"              # Primary testing framework
pytest-asyncio = "^0.23.0"     # Async test support
pytest-mock = "^3.14.0"        # Simplified mocking via mocker fixture
pytest-cov = "^6.2.0"          # Coverage reporting
hypothesis = "^6.138.3"        # Property-based testing
```

### Why pytest Over unittest

| Feature | pytest | unittest |
|---------|--------|----------|
| **Syntax** | Clean `assert` statements | Verbose `self.assertEqual()` |
| **Fixtures** | Powerful, reusable fixtures | Complex setUp/tearDown |
| **Mocking** | `mocker` fixture via pytest-mock | Manual import/context managers |
| **Parameterization** | Built-in `@pytest.mark.parametrize` | Limited support |
| **Error Reports** | Detailed assertion introspection | Generic failure messages |

---

## 📋 TEST STRUCTURE STANDARDS

### Arrange-Act-Assert (AAA) Pattern

**Every test must follow AAA structure:**

```python
# CORRECT - AAA Pattern Example
def test_given_valid_contract_when_loading_then_returns_contract_instance(
    contract_factory: DynamicAgentContractFactory,
    valid_contract_path: Path
) -> None:
    """Test contract loading with valid YAML configuration."""
    
    # ARRANGE - Set up test environment
    expected_contract_id = "analysis_agent_v1"
    expected_version = "1.0.0"
    
    # ACT - Execute the specific behavior being tested
    contract = contract_factory.load_agent_contract(valid_contract_path)
    
    # ASSERT - Verify the expected outcome
    assert contract.contract_id == expected_contract_id
    assert contract.version == expected_version
    assert len(contract.preconditions) > 0
    assert contract.ltl_formulas_valid is True
```

### Test Naming Convention

**Use descriptive GIVEN-WHEN-THEN format:**

```python
# CORRECT - Descriptive test names
def test_given_missing_contract_file_when_loading_contract_then_raises_file_not_found_error()
def test_given_invalid_ltl_formula_when_validating_contract_then_raises_validation_error()
def test_given_multiple_agents_when_orchestrating_workflow_then_coordinates_execution_sequentially()

# FORBIDDEN - Generic test names
def test_contract_loading()
def test_validation()
def test_orchestration()
```

### Project Structure

```
tests/
├── unit/                          # Fast, isolated unit tests
│   ├── test_contract_factory.py
│   ├── test_ltl_model_checker.py
│   └── test_agent_implementations.py
├── integration/                   # Component interaction tests
│   ├── test_agent_orchestration.py
│   ├── test_workflow_execution.py
│   └── test_validation_pipeline.py
├── e2e/                          # End-to-end workflow tests
│   ├── test_complete_development_workflow.py
│   └── test_contract_evolution_cycle.py
├── fixtures/                     # Shared test data
│   ├── contracts/
│   │   ├── valid_analysis_contract.yaml
│   │   └── invalid_contract.yaml
│   └── test_data.py
└── conftest.py                   # Pytest configuration and fixtures
```

---

## 🔍 TEST DOUBLE STRATEGY

### Precise Test Double Taxonomy

| Test Double | Purpose | When to Use | Example |
|-------------|---------|-------------|---------|
| **Dummy** | Fill parameter lists | Required parameter not relevant to test | `DummyAgent()` for interface compliance |
| **Fake** | Lightweight working implementation | Complex state without external dependencies | `InMemoryContractStore()` |
| **Stub** | Provide canned answers | Control return values for state verification | `StubClaudeClient.return_value = "analysis"` |
| **Spy** | Record interaction information | Need to verify calls were made | `spy.verify_called_with(expected_args)` |
| **Mock** | Verify expected interactions | Core test purpose is interaction verification | `mock.assert_called_once_with(contract)` |

### Strategic Mocking Guidelines

#### ✅ MOCK THESE (External/Slow/Non-deterministic):
```python
# External API calls
mocker.patch("anthropic.Anthropic")

# File system operations (when testing logic, not I/O)
mocker.patch("pathlib.Path.exists", return_value=True)

# Time-dependent operations
mocker.patch("time.time", return_value=1234567890)

# Network operations
mocker.patch("httpx.AsyncClient.post")
```

#### 🚫 DON'T MOCK THESE (Fast/Deterministic/Internal):
```python
# Internal domain objects - use real instances
contract = AgentContract(contract_id="test", version="1.0.0")

# Configuration objects - use real objects
config = AgentConfig(claude_model="test-model", timeout=30)

# Data structures - use real objects
context = TaskContext(task_id="test", module_name="test_module")

# Simple calculations - use real implementations
result = calculator.calculate_score(data)  # Don't mock simple logic
```

### Mocking Implementation Examples

```python
import pytest
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock

class TestAgentOrchestrator:
    
    async def test_orchestration_with_real_objects_when_possible(
        self,
        orchestrator: AgentOrchestrator,
        real_agent_config: AgentConfig
    ) -> None:
        """Use real objects for fast, deterministic dependencies."""
        # Arrange - Real objects for internal components
        request = DevelopmentRequest(
            request_id="test-123",
            module_name="test_module",
            requirements=["Build validation system"]
        )
        
        # Act
        result = await orchestrator.orchestrate_workflow(request)
        
        # Assert
        assert result.success is True
        assert result.phases_completed == ["analysis", "validation"]
    
    async def test_orchestration_mocks_external_claude_api(
        self,
        orchestrator: AgentOrchestrator,
        mocker: MockerFixture
    ) -> None:
        """Mock only slow external dependencies (Claude API)."""
        # Arrange - Mock external API
        mock_claude = mocker.patch("anthropic.Anthropic")
        mock_response = AsyncMock()
        mock_response.content = [AsyncMock(text="Valid analysis result")]
        mock_claude.return_value.messages.create.return_value = mock_response
        
        request = DevelopmentRequest(
            request_id="test-456",
            module_name="test_module",
            requirements=["Build validation system"]
        )
        
        # Act
        result = await orchestrator.orchestrate_workflow(request)
        
        # Assert - Verify both outcome and interaction
        assert result.success is True
        mock_claude.return_value.messages.create.assert_called_once()
        call_args = mock_claude.return_value.messages.create.call_args
        assert call_args[1]["model"] == "claude-3-sonnet-20240229"
```

---

## 🧪 TEST IMPLEMENTATION PATTERNS

### Unit Testing Patterns

```python
class TestDynamicAgentContractFactory:
    """Test suite for contract factory functionality."""
    
    def test_contract_loading_success_path(
        self,
        contract_factory: DynamicAgentContractFactory,
        valid_contract_yaml: str,
        tmp_path: Path
    ) -> None:
        """Test successful contract loading from valid YAML."""
        # Arrange
        contract_file = tmp_path / "test_contract.yaml"
        contract_file.write_text(valid_contract_yaml)
        
        # Act
        contract = contract_factory.load_agent_contract(contract_file)
        
        # Assert
        assert contract.contract_id == "test_agent_v1"
        assert len(contract.preconditions) == 2
        assert all(condition.ltl_formula for condition in contract.preconditions)
    
    def test_contract_loading_error_conditions(
        self,
        contract_factory: DynamicAgentContractFactory
    ) -> None:
        """Test error handling for various failure conditions."""
        # Test missing file
        with pytest.raises(FileNotFoundError, match="not found"):
            contract_factory.load_agent_contract(Path("/nonexistent/file.yaml"))
        
        # Test invalid YAML (via temporary file)
        invalid_yaml = "invalid: yaml: content: ["
        tmp_file = tmp_path / "invalid.yaml"
        tmp_file.write_text(invalid_yaml)
        
        with pytest.raises(YAMLError, match="Invalid YAML"):
            contract_factory.load_agent_contract(tmp_file)
```

### Integration Testing Patterns

```python
class TestAgentWorkflowIntegration:
    """Integration tests for complete agent workflow execution."""
    
    async def test_analysis_to_verification_workflow_integration(
        self,
        orchestrator: GoverningDevelopmentRuleEngine,
        analysis_agent: ConfigurableAnalysisAgent,
        verification_agent: LTLVerificationAgent,
        development_request: DevelopmentRequest
    ) -> None:
        """Test complete workflow from analysis through verification."""
        # Arrange - Real component integration
        workflow_context = WorkflowContext(
            request=development_request,
            agents=[analysis_agent, verification_agent],
            quality_gates_enabled=True
        )
        
        # Act - Execute complete workflow
        result = await orchestrator.orchestrate_development_lifecycle(
            development_request
        )
        
        # Assert - Verify workflow completion and quality
        assert result.success is True
        assert result.lifecycle_phase == DevelopmentPhase.READY_FOR_IMPLEMENTATION
        assert result.verified_specification is not None
        assert len(result.verified_specification.ltl_constraints) > 0
        
        # Verify agent coordination
        assert result.orchestration_metadata.phases_completed == [
            "pre_analysis", "analysis", "verification"
        ]
        assert result.orchestration_metadata.agents_coordinated >= 2
```

### Property-Based Testing for Complex Logic

```python
from hypothesis import given, strategies as st

class TestLTLFormulaValidation:
    """Property-based tests for LTL formula validation."""
    
    @given(
        formula=st.text(
            alphabet="□◇∧∨→¬()ABCDEFabcdef ",
            min_size=5,
            max_size=50
        )
    )
    def test_ltl_formula_validation_properties(
        self,
        ltl_validator: LTLFormulaValidator,
        formula: str
    ) -> None:
        """Test LTL validation behaves consistently for generated formulas."""
        # Act
        result = ltl_validator.validate_formula(formula)
        
        # Assert - Properties that should always hold
        assert isinstance(result.is_valid, bool)
        if result.is_valid:
            assert result.parsed_formula is not None
            assert result.error_message is None
        else:
            assert result.parsed_formula is None
            assert result.error_message is not None
            assert len(result.error_message) > 0
```

---

## 📊 COVERAGE & QUALITY METRICS

### Coverage Requirements

```toml
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "-v",                         # Verbose output
    "--tb=short",                # Short traceback format
    "--cov=development_orchestration",  # Coverage package
    "--cov-report=term",         # Terminal coverage report
    "--cov-report=html",         # HTML coverage report
    "--cov-fail-under=90",       # Fail if coverage < 90%
    "--cov-branch",              # Branch coverage
]
asyncio_mode = "auto"            # Automatic async test detection
```

### Quality Gates

**Required Coverage Thresholds:**
- **Overall Coverage**: ≥ 90%
- **Branch Coverage**: ≥ 85%
- **Critical Modules** (orchestration, validation): ≥ 95%
- **Test Suite Performance**: < 30 seconds for full run

**Code Quality Metrics:**
- **Cyclomatic Complexity**: ≤ 10 per function
- **Test-to-Code Ratio**: ≥ 1:1 (equal or more test code than production)
- **Mutation Testing Score**: ≥ 80% (if using mutation testing)

---

## 🚀 TESTING WORKFLOW INTEGRATION

### Pre-Commit Testing

```bash
# .pre-commit-config.yaml example
repos:
  - repo: local
    hooks:
      - id: pytest-fast
        name: Fast unit tests
        entry: pytest tests/unit/ -x --disable-warnings
        language: system
        pass_filenames: false
        
      - id: mypy-check
        name: Type checking
        entry: mypy src/ tests/
        language: system
        pass_filenames: false
```

### CI/CD Testing Pipeline

```yaml
# Example GitHub Actions workflow
name: AI Agent Testing Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.13]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install poetry
        poetry install
    
    - name: Run static analysis
      run: |
        poetry run mypy src/ tests/
        poetry run ruff check src/ tests/
    
    - name: Run unit tests
      run: |
        poetry run pytest tests/unit/ --cov --cov-fail-under=90
    
    - name: Run integration tests
      run: |
        poetry run pytest tests/integration/ --cov-append
    
    - name: Run E2E tests
      run: |
        poetry run pytest tests/e2e/ --cov-append
        
    - name: Generate coverage report
      run: |
        poetry run coverage html
        poetry run coverage report
```

### Performance Testing Integration

```python
import pytest
import time
from typing import Dict, Any

class TestAgentPerformance:
    """Performance testing for agent operations."""
    
    @pytest.mark.performance
    async def test_contract_loading_performance(
        self,
        contract_factory: DynamicAgentContractFactory,
        performance_contract_path: Path
    ) -> None:
        """Test contract loading performance meets requirements."""
        # Arrange
        max_loading_time = 0.1  # 100ms requirement
        
        # Act & Time
        start_time = time.perf_counter()
        contract = contract_factory.load_agent_contract(performance_contract_path)
        end_time = time.perf_counter()
        
        # Assert
        loading_time = end_time - start_time
        assert loading_time < max_loading_time, \
            f"Contract loading took {loading_time:.3f}s, exceeds {max_loading_time}s limit"
        assert contract is not None
    
    @pytest.mark.performance
    async def test_ltl_verification_performance(
        self,
        ltl_verifier: LTLVerificationAgent,
        large_execution_trace: ExecutionTrace,
        complex_ltl_formulas: List[LTLFormula]
    ) -> None:
        """Test LTL verification performance with complex constraints."""
        # Performance requirement: < 500ms for complex verification
        max_verification_time = 0.5
        
        start_time = time.perf_counter()
        result = await ltl_verifier.verify_execution_trace(
            large_execution_trace,
            complex_ltl_formulas
        )
        end_time = time.perf_counter()
        
        verification_time = end_time - start_time
        assert verification_time < max_verification_time, \
            f"LTL verification took {verification_time:.3f}s, exceeds {max_verification_time}s limit"
        assert result.constraints_satisfied is not None
```

---

## 🎯 SUCCESS CRITERIA

### Test Quality Gates

**Before Code Merge:**
- [ ] All tests passing (unit, integration, E2E)
- [ ] Coverage ≥ 90% overall, ≥ 95% for critical modules
- [ ] No test doubles used where real objects are feasible
- [ ] All tests follow AAA pattern with descriptive names
- [ ] Performance requirements met for critical paths
- [ ] Static analysis passing (mypy, linting)

**Production Readiness:**
- [ ] Complete test suite execution < 30 seconds
- [ ] Contract loading performance < 100ms
- [ ] LTL verification performance < 500ms
- [ ] Agent orchestration end-to-end < 2 seconds
- [ ] Zero test failures in production environment
- [ ] Comprehensive error condition coverage

### Test Maintenance

**Monthly Reviews:**
- Identify and refactor brittle tests
- Review mock usage - replace with real objects where possible
- Update performance benchmarks
- Clean up obsolete test scenarios

**Continuous Improvement:**
- Add integration tests when bugs found in production
- Enhance property-based testing coverage
- Implement mutation testing for critical modules
- Monitor and optimize test execution performance

This testing strategy ensures our AI agent governance system meets the highest quality standards while maintaining development velocity and confidence in system reliability.