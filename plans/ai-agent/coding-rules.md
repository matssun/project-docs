# AI Agent Implementation: Comprehensive Coding Rules

## Overview

This document consolidates all coding standards and rules that MUST be followed during the AI agent governance system implementation. These rules are extracted from our existing codebase standards and are **non-negotiable** requirements for code quality, system reliability, and architectural compliance.

---

## 🚨 CRITICAL RULES - IMMEDIATE FAILURE IF VIOLATED

### 1. Import Rules - **ZERO TOLERANCE**

**Rule**: NO conditional imports, NO try/except around imports, NO optional dependencies in production code.

#### ❌ FORBIDDEN PATTERNS
```python
# FORBIDDEN - Hides import failures
try:
    from some_library import SomeClass
    LIBRARY_AVAILABLE = True
except ImportError:
    class SomeClass:
        pass
    LIBRARY_AVAILABLE = False

# FORBIDDEN - Silent import failures
try:
    import optional_library
except ImportError:
    optional_library = None

# FORBIDDEN - Runtime conditional behavior
HAS_REDIS = False
try:
    import redis
    HAS_REDIS = True
except ImportError:
    pass
```

#### ✅ REQUIRED PATTERNS
```python
# CORRECT - Import fails immediately if not available
from anthropic import Anthropic
from error_handling import ErrorFactory
from validation import ValidationManager
import yaml
import logging

# All dependencies declared in pyproject.toml
[tool.poetry.dependencies]
anthropic = "^0.25.0"
pyyaml = "^6.0.2"
```

**Enforcement**: Any PR with conditional imports will be **automatically rejected**.

### 2. Architecture Compliance Rules

#### Core Principles
- **ALWAYS** use protocols from core_interfaces
- **ALWAYS** use error_handling module for ALL errors  
- **ALWAYS** follow object-oriented analysis and design principles
- **ALWAYS** use fully typed objects - NO untyped data structures or metadata
- **NEVER** use `Any`, `hasattr`, `getattr`, `setattr`
- **NEVER** use `Dict[str, Any]` or untyped dictionaries for data
- **NEVER** create circular dependencies

#### Object-Oriented Design Enforcement

**FORBIDDEN: Untyped Data Structures**
```python
# FORBIDDEN - Untyped dictionary metadata
metadata = {
    "timestamp": time.time(),
    "agent_id": "analysis_agent", 
    "execution_data": some_complex_data,
    "custom_fields": {"key": "value"}  # Untyped nested data
}

# FORBIDDEN - Generic Dict[str, Any] usage
def process_agent_data(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"result": data.get("input", "default")}

# FORBIDDEN - Untyped configuration
config = {
    "claude_model": "claude-3-sonnet",
    "max_tokens": 4000,
    "agent_settings": {"timeout": 300}  # Nested untyped data
}
```

**REQUIRED: Fully Typed Objects**
```python
# CORRECT - Typed data classes
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass(frozen=True)
class AgentExecutionMetadata:
    """Fully typed metadata for agent execution tracking."""
    timestamp: datetime
    agent_id: str
    execution_duration_seconds: float
    task_complexity_score: int
    memory_usage_mb: Optional[float] = None
    custom_attributes: Optional[List[CustomAttribute]] = None

@dataclass(frozen=True) 
class CustomAttribute:
    """Typed custom attribute structure."""
    name: str
    value: str
    attribute_type: str

# CORRECT - Typed configuration objects
from pydantic import BaseModel, Field

class AgentConfiguration(BaseModel):
    """Fully typed agent configuration."""
    claude_model: str = Field(..., description="Claude model identifier")
    max_tokens: int = Field(4000, ge=1, le=100000)
    temperature: float = Field(0.0, ge=0.0, le=2.0)
    timeout_seconds: int = Field(300, ge=1)
    
    class Config:
        extra = "forbid"  # Prevent untyped additions
        validate_assignment = True

# CORRECT - Typed function signatures
def process_agent_execution(
    execution_data: AgentExecutionData,
    metadata: AgentExecutionMetadata
) -> AgentExecutionResult:
    """Process agent execution with fully typed parameters."""
    return AgentExecutionResult(
        success=True,
        result_data=execution_data.output,
        metadata=metadata
    )
```

#### Mandatory Typing Patterns

**Value Objects for Complex Data:**
```python
# CORRECT - Domain-specific value objects
@dataclass(frozen=True)
class LTLConstraint:
    """Linear Temporal Logic constraint specification."""
    constraint_id: str
    formula: str
    description: str
    severity: ConstraintSeverity
    validation_method: ValidationMethod

@dataclass(frozen=True)
class TaskContext:
    """Comprehensive task execution context."""
    task_id: str
    module_name: str
    phase: DevelopmentPhase
    requirements: RequirementSpecification
    constraints: List[LTLConstraint]
    dependencies: List[ModuleDependency]
    execution_metadata: Optional[AgentExecutionMetadata] = None

# CORRECT - Enum-based type safety
from enum import Enum

class ConstraintSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class ValidationMethod(Enum):
    SCHEMA_CHECK = "schema_check"
    LTL_VERIFICATION = "ltl_verification"
    CUSTOM_VALIDATOR = "custom_validator"
```

**Protocol-Based Design:**
```python
# CORRECT - Typed protocols for abstractions
from typing import Protocol

class AgentContractProtocol(Protocol):
    """Protocol for agent contract behavior."""
    
    @property
    def contract_id(self) -> str: ...
    
    @property
    def version(self) -> str: ...
    
    @property
    def preconditions(self) -> List[ContractCondition]: ...
    
    def validate_execution_trace(
        self, 
        trace: ExecutionTrace
    ) -> ContractValidationResult: ...

# CORRECT - Concrete implementation with full typing
class YAMLAgentContract(AgentContractProtocol):
    """YAML-based agent contract implementation."""
    
    def __init__(
        self,
        contract_config: AgentContractConfig,
        validator: ContractValidator
    ) -> None:
        self._config = contract_config
        self._validator = validator
    
    @property
    def contract_id(self) -> str:
        return self._config.contract_id
    
    def validate_execution_trace(
        self, 
        trace: ExecutionTrace
    ) -> ContractValidationResult:
        # Full type safety throughout implementation
        violations = []
        for condition in self._config.preconditions:
            result = self._validator.check_condition(condition, trace)
            if not result.satisfied:
                violations.append(
                    ContractViolation(
                        condition_id=condition.condition_id,
                        violation_type=result.violation_type,
                        description=result.description
                    )
                )
        
        return ContractValidationResult(
            contract_compliant=len(violations) == 0,
            violations=violations,
            validation_timestamp=datetime.utcnow()
        )
```

#### Exception Process: When to Request Permission

**STOP AND ASK if you need to:**
1. Use `Dict[str, Any]` for external API responses (before parsing to typed objects)
2. Use `Any` for generic type parameters in abstract base classes
3. Use untyped data for temporary debugging or migration phases
4. Interface with external libraries that don't provide type hints

**Request Template:**
```
TYPING EXCEPTION REQUEST:
- **Context**: [Where and why you need untyped data]
- **Duration**: [Temporary/Permanent]
- **Mitigation**: [How you'll minimize type safety impact] 
- **Migration Plan**: [If temporary, how you'll convert to typed]
```

#### Interface-Driven Design
```python
# CORRECT - Protocol-based design
from core_interfaces import ValidationProtocol
from error_handling import ErrorFactory

class AgentValidationManager(ValidationProtocol):
    def __init__(self, error_factory: ErrorFactory):
        self._error_factory = error_factory
    
    async def validate(self, data: Any) -> ValidationResult:
        try:
            # Validation logic
            return ValidationResult(is_valid=True)
        except Exception as e:
            # Use error_handling for ALL errors
            error = self._error_factory.create_validation_error(
                "Agent validation failed", {"data": str(data), "error": str(e)}
            )
            raise error
```

#### Dependency Hierarchy Compliance
```
Foundation Layer (core_interfaces, core_data_structures, error_handling)
    ↓
Core Services Layer (validation, config_management, client_base)
    ↓  
Infrastructure Layer (service_infrastructure, monitoring_infrastructure)
    ↓
Domain Layer (development_orchestration agents)
```

**Rule**: Lower layers CANNOT import from higher layers. No circular dependencies.

### 3. Error Handling Rules

#### Mandatory Error Handling Patterns
```python
# CORRECT - All errors through error_handling module
from error_handling import ErrorFactory

class MyAgent:
    def __init__(self, error_factory: ErrorFactory):
        self._error_factory = error_factory
    
    def process_data(self, data: Dict[str, Any]) -> ProcessingResult:
        try:
            # Processing logic
            return ProcessingResult(success=True)
        except ValidationError as e:
            # Specific error handling
            error = self._error_factory.create_validation_error(
                "Data processing validation failed", 
                {"data": data, "validation_error": str(e)}
            )
            raise error
        except Exception as e:
            # General error handling
            error = self._error_factory.create_processing_error(
                "Unexpected error during data processing",
                {"data": data, "error": str(e)}
            )
            raise error
```

#### Forbidden Error Patterns
```python
# FORBIDDEN - Raw exception raising
raise ValueError("Something went wrong")

# FORBIDDEN - Silent error handling
try:
    risky_operation()
except Exception:
    pass  # Silent failure

# FORBIDDEN - Generic exception catching without error factory
try:
    operation()
except Exception as e:
    print(f"Error: {e}")  # No proper error handling
```

---

## 🏗️ ARCHITECTURAL RULES

### 4. Agent Implementation Standards

#### Base Agent Pattern
```python
# CORRECT - Agent implementation pattern
from abc import abstractmethod
from anthropic import Anthropic
from core_interfaces import DevelopmentAgentProtocol
from error_handling import ErrorFactory
from config_management import CommonSettings

class BaseDevelopmentAgent(DevelopmentAgentProtocol):
    def __init__(
        self,
        claude_client: Anthropic,
        config_manager: CommonSettings,
        error_factory: ErrorFactory,
        **kwargs: Any
    ):
        self._claude = claude_client
        self._config = config_manager
        self._error_factory = error_factory
        
    @abstractmethod
    async def process_task(self, task_id: str, context: TaskContext) -> TaskResult:
        """Process development task - must be implemented by subclasses."""
        ...
    
    @abstractmethod
    async def validate_prerequisites(self, context: TaskContext) -> bool:
        """Validate prerequisites - must be implemented by subclasses."""
        ...
```

#### Agent Contract Loading
```python
# CORRECT - Dynamic contract loading
from pathlib import Path
from typing import Union
import yaml

class DynamicAgentContractFactory:
    def load_agent_contract(
        self,
        contract_path: Union[str, Path]
    ) -> AgentContract:
        """Load agent contract from YAML configuration."""
        contract_path = Path(contract_path)
        
        if not contract_path.exists():
            error = self._error_factory.create_file_not_found_error(
                f"Agent contract file not found: {contract_path}"
            )
            raise error
        
        try:
            with open(contract_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            return self._create_contract_instance(config_data)
            
        except yaml.YAMLError as e:
            error = self._error_factory.create_parsing_error(
                f"Invalid YAML in contract file {contract_path}",
                {"yaml_error": str(e)}
            )
            raise error
```

### 5. Validation System Rules

#### ValidationManager-Centered Architecture

**CRITICAL**: ValidationManager is the **single coordination point** for all validation activities. This is the primary interface that service developers interact with.

```python
# CORRECT - ValidationManager usage pattern
from validation import ValidationManager
from error_handling import ErrorFactory

class OrderProcessingService:
    def __init__(self, error_factory: ErrorFactory):
        # Create ValidationManager once at service startup
        self.validation_manager = ValidationManager("order_processing")
        self.validation_manager.add_rule(RequiredFieldRule("customer_id"))
        self.validation_manager.add_rule(EmailFormatRule("customer_email"))
        self._error_factory = error_factory

    async def process_order(self, order_data: dict) -> None:
        # Use ValidationManager for all validation
        result = self.validation_manager.validate(order_data)
        
        if not result.is_successful():
            # Error handling automatically integrated via bridge pattern
            self._handle_validation_errors(result.issues)
        
        # Pass validation context to lower layers
        context = self.validation_manager.get_context()
        await self.database_manager.save_order(order_data, validation_context=context)
```

#### Validation Context Lifecycle Strategy

**RULE**: ValidationManager is created **once at service startup**, contexts are passed down through application layers.

**Context Flow Pattern**: `Service → DatabaseManager → Backend operations`

```python
# CORRECT - Context passing through layers
class DatabaseManager:
    async def save_order(self, order_data: dict, validation_context: IValidationContext) -> None:
        # Receive context from above, create child contexts as needed
        db_context = validation_context.create_child("database_validation")
        
        # Pass to backend operations
        await self.order_repository.validate_and_save(order_data, db_context)

class OrderRepository:
    async def validate_and_save(self, order_data: dict, context: IValidationContext) -> None:
        # Use received context for validation operations
        field_context = context.create_child("order_fields")
        # Perform validation with context
```

#### Forbidden ValidationManager Patterns

```python
# FORBIDDEN - Creating ValidationManager at mid-level
class DatabaseManager:
    async def save_order(self, order_data: dict) -> None:
        # ❌ NEVER create ValidationManager at mid-level services
        validation_manager = ValidationManager("db_validation")  # WRONG
        
# FORBIDDEN - Bypassing ValidationManager
from validation.factories import ValidationFactory
from validation.process import ValidationProcess

class SomeService:
    def __init__(self):
        # ❌ NEVER use ValidationFactory directly
        self.factory = ValidationFactory()  # WRONG
        
        # ❌ NEVER use ValidationProcess directly  
        self.process = ValidationProcess()   # WRONG

# FORBIDDEN - Manual bridge handling
from validation.context import ValidationToErrorContextBridge

class SomeService:
    def handle_errors(self, validation_context):
        # ❌ NEVER handle bridge manually - ValidationManager does this
        bridge = ValidationToErrorContextBridge()  # WRONG
        error_context = bridge.convert(validation_context)  # WRONG
```

#### Info Object Ownership Rules

**CRITICAL**: The validation module owns the creation and lifecycle of **ALL Info objects** and **ErrorRecord objects**.

```python
# CORRECT - Info object creation in validation module
from validation import ValidationManager, InfoFactory
from error_handling import ErrorFactory

class ValidationService:
    def __init__(self, error_factory: ErrorFactory):
        self.validation_manager = ValidationManager("service_validation")
        self.info_factory = InfoFactory()
        self._error_factory = error_factory
    
    async def validate_with_info_objects(self, data: dict) -> None:
        try:
            result = self.validation_manager.validate(data)
            
            if not result.is_successful():
                # Validation module creates ALL Info objects
                context = self.validation_manager.get_context()
                
                # Extract Info objects AND ErrorRecord using InfoFactory
                validation_info = self.info_factory.extract_validation_info(context)
                security_info = self.info_factory.extract_security_info(context)
                schema_info = self.info_factory.extract_schema_info(context)
                error_record = self.info_factory.extract_error_record(context)
                
                # Create complete ErrorState with ErrorRecord + Info interfaces
                error_state = ErrorState(
                    error_record=error_record,
                    validation_info=validation_info,
                    security_info=security_info,
                    schema_info=schema_info
                )
                
                # Provide ErrorState to error handling through bridge
                error = self._error_factory.create_validation_error_with_state(
                    "Validation failed with complete context",
                    error_state
                )
                raise error
                
        except Exception as e:
            # ValidationManager automatically handles error conversion via bridge
            raise
```

#### Mandatory Validation Integration Rules

```python
# CORRECT - Complete validation integration
class AgentValidationManager:
    def __init__(self, error_factory: ErrorFactory):
        # Create ValidationManager at initialization
        self.validation_manager = ValidationManager("agent_execution")
        self.info_factory = InfoFactory()
        self._error_factory = error_factory
        
        # Add agent-specific validation rules
        self.validation_manager.add_rule(ContractComplianceRule())
        self.validation_manager.add_rule(LTLFormulaRule())
        self.validation_manager.add_rule(SecurityConstraintRule())
    
    async def validate_agent_execution(
        self, 
        execution_trace: AgentExecutionTrace
    ) -> AgentExecutionValidationResult:
        """Validate agent execution with complete error state creation."""
        
        # Use ValidationManager for all validation
        result = self.validation_manager.validate(execution_trace.to_dict())
        
        if result.is_successful():
            return AgentExecutionValidationResult(
                valid=True,
                execution_trace=execution_trace
            )
        
        # Create complete error information using validation module
        context = self.validation_manager.get_context()
        
        # Validation module creates ALL Info objects
        validation_info = self.info_factory.extract_validation_info(context)
        security_info = self.info_factory.extract_security_info(context)
        contract_info = self.info_factory.extract_contract_info(context)
        error_record = self.info_factory.extract_error_record(context)
        
        # Create complete ErrorState
        error_state = ErrorState(
            error_record=error_record,
            validation_info=validation_info,
            security_info=security_info,
            contract_info=contract_info
        )
        
        # Error factory uses complete ErrorState
        error = self._error_factory.create_agent_validation_error(
            "Agent execution validation failed",
            error_state
        )
        
        raise error

# CORRECT - XML validation with ValidationManager
class XMLValidationService:
    def __init__(self):
        self.validation_manager = ValidationManager("xml_validation")
    
    async def validate_xml_document(
        self, 
        xml_content: str, 
        schema_url: str
    ) -> XMLValidationResult:
        """Use ValidationManager convenience method for XML validation."""
        
        # ValidationManager handles all XML validation complexity
        result = self.validation_manager.validate_xml_document(
            data=xml_content,
            schema_url=schema_url,
            field_path=FieldPath("api.request.xml")
        )
        
        return XMLValidationResult(
            valid=result.is_successful(),
            issues=result.issues
        )
```

#### Architecture Compliance Rules

- **ALWAYS** use ValidationManager as the primary interface at the highest application level
- **ALWAYS** create ValidationManager with descriptive context names at service startup  
- **ALWAYS** pass validation contexts down through application layers
- **ALWAYS** use ValidationManager convenience methods (`validate_xml_document`, `validate_json_request`)
- **ALWAYS** let ValidationManager handle error conversion through bridge pattern
- **ALWAYS** use validation module to create ALL Info objects and ErrorRecord objects
- **NEVER** create ValidationManager instances at mid-level services - receive contexts from above
- **NEVER** instantiate ValidationFactory, ValidationProcess, or ValidationOrchestrator directly
- **NEVER** bypass ValidationManager for direct component usage
- **NEVER** handle ValidationToErrorContextBridge manually
- **NEVER** allow error handling module to create Info objects or ErrorRecord objects
- **NEVER** export concrete validation classes - only provide through interface boundaries

### 6. Configuration Management Rules

#### YAML Configuration Standards
```yaml
# CORRECT - Agent contract YAML structure
agent_contract:
  contract_id: "analysis_agent_v1"
  version: "1.2.0"
  
  preconditions:
    - name: "valid_requirements"
      ltl_formula: "□(HasRequirements ∧ ValidFormat)"
      validation_method: "schema_check"
      required: true
      
  pathconditions:
    - name: "approved_tools_only"
      ltl_formula: "□(ToolUse → ApprovedTools)"
      monitoring: "real_time"
      violation_action: "halt"
      
  postconditions:
    - name: "complete_analysis"
      ltl_formula: "◇(RequirementsComplete ∧ DomainModelValid)"
      verification_agent: "ltl_verification_agent"
      
  performance_requirements:
    task_completion_rate:
      threshold: "> 95%"
      measurement_window: "7d"
```

#### Configuration Loading Standards
```python
# CORRECT - Configuration validation
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AgentContractConfig(BaseModel):
    contract_id: str = Field(..., description="Unique contract identifier")
    version: str = Field(..., regex=r"^\d+\.\d+\.\d+$")
    preconditions: List[ContractCondition]
    pathconditions: List[ContractCondition] 
    postconditions: List[ContractCondition]
    
    class Config:
        extra = "forbid"  # Prevent unknown fields
        validate_assignment = True
```

---

## 📝 CODE QUALITY RULES

### 7. Type Annotations - **MANDATORY**

```python
# CORRECT - Full type annotations
from typing import Dict, List, Optional, Any, Protocol
from abc import abstractmethod

class AgentProtocol(Protocol):
    @abstractmethod
    async def process_task(
        self, 
        task_id: str, 
        context: TaskContext
    ) -> TaskResult:
        """Process a development task."""
        ...

class ConcreteAgent:
    def __init__(self, config: AgentConfig) -> None:
        self._config = config
    
    async def process_task(
        self, 
        task_id: str, 
        context: TaskContext
    ) -> TaskResult:
        # Implementation
        return TaskResult(task_id=task_id, status=TaskStatus.COMPLETED)
```

### 8. Logging Standards

```python
# CORRECT - Structured logging
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    async def orchestrate_workflow(
        self, 
        request: DevelopmentRequest
    ) -> OrchestrationResult:
        logger.info(
            "Starting workflow orchestration",
            extra={
                "request_id": request.request_id,
                "module_name": request.module_name,
                "complexity_level": request.complexity_level
            }
        )
        
        try:
            result = await self._execute_workflow(request)
            
            logger.info(
                "Workflow orchestration completed successfully",
                extra={
                    "request_id": request.request_id,
                    "execution_duration": result.execution_duration,
                    "phases_completed": result.phases_completed
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Workflow orchestration failed",
                extra={
                    "request_id": request.request_id,
                    "error": str(e),
                    "error_type": type(e).__name__
                },
                exc_info=True
            )
            raise
```

### 9. Documentation Standards

```python
# CORRECT - Comprehensive docstrings
class LTLModelChecker:
    """Linear Temporal Logic model checker for agent contract validation.
    
    This class implements formal verification of agent execution traces
    against LTL specifications defined in agent contracts.
    
    Attributes:
        _formula_parser: Parser for LTL formula syntax
        _model_checker: Core LTL model checking engine
        
    Example:
        >>> checker = LTLModelChecker(config)
        >>> result = await checker.verify_execution_trace(trace, formulas)
        >>> assert result.constraints_satisfied
    """
    
    def __init__(self, config: ModelCheckerConfig) -> None:
        """Initialize LTL model checker with configuration.
        
        Args:
            config: Configuration for model checker behavior
            
        Raises:
            ConfigurationError: If config is invalid
        """
        self._config = config
        
    async def verify_execution_trace(
        self,
        execution_trace: ExecutionTrace,
        ltl_formulas: List[LTLFormula]
    ) -> LTLVerificationResult:
        """Verify execution trace against LTL formulas.
        
        Args:
            execution_trace: Trace of agent execution steps
            ltl_formulas: List of LTL formulas to verify against
            
        Returns:
            LTLVerificationResult containing verification outcome
            
        Raises:
            VerificationError: If verification process fails
            InvalidFormulaError: If LTL formula syntax is invalid
        """
        # Implementation
        pass
```

---

## 🧪 TESTING RULES

### 10. Test Structure Standards

```python
# CORRECT - Test structure following AAA pattern
import pytest
from unittest.mock import Mock
from typing import Dict, Any

class TestAgentContractFactory:
    """Test suite for DynamicAgentContractFactory."""
    
    def test_given_valid_contract_yaml_when_loading_contract_then_returns_valid_contract(
        self,
        contract_factory: DynamicAgentContractFactory,
        valid_contract_path: Path
    ) -> None:
        """Test contract loading with valid YAML file."""
        # Arrange
        expected_contract_id = "test_agent_v1"
        
        # Act
        contract = contract_factory.load_agent_contract(valid_contract_path)
        
        # Assert
        assert contract.contract_id == expected_contract_id
        assert contract.version == "1.0.0"
        assert len(contract.preconditions) > 0
        
    def test_given_missing_contract_file_when_loading_contract_then_raises_file_not_found_error(
        self,
        contract_factory: DynamicAgentContractFactory
    ) -> None:
        """Test contract loading with missing file."""
        # Arrange
        missing_path = Path("/nonexistent/contract.yaml")
        
        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            contract_factory.load_agent_contract(missing_path)
        
        assert "not found" in str(exc_info.value)
```

### 11. Mock Usage Rules

```python
# CORRECT - Limited, strategic mocking
import pytest
from pytest_mock import MockerFixture

class TestAgentOrchestrator:
    async def test_orchestration_with_real_objects(
        self,
        orchestrator: AgentOrchestrator,
        valid_request: DevelopmentRequest
    ) -> None:
        """Test orchestration using real objects where possible."""
        # Arrange - use real objects for fast, deterministic dependencies
        
        # Act
        result = await orchestrator.orchestrate_workflow(valid_request)
        
        # Assert
        assert result.success is True
        
    async def test_orchestration_with_external_service_mock(
        self,
        orchestrator: AgentOrchestrator,
        valid_request: DevelopmentRequest,
        mocker: MockerFixture
    ) -> None:
        """Test orchestration mocking only slow external dependencies."""
        # Arrange - mock only the slow external service
        mock_claude_client = mocker.patch("anthropic.Anthropic")
        mock_claude_client.return_value.messages.create.return_value = Mock(
            content=[Mock(text="Valid analysis result")]
        )
        
        # Act
        result = await orchestrator.orchestrate_workflow(valid_request)
        
        # Assert
        assert result.success is True
        mock_claude_client.return_value.messages.create.assert_called_once()
```

---

## 🔧 PERFORMANCE RULES

### 12. Async/Await Standards

```python
# CORRECT - Proper async patterns
import asyncio
from typing import List, Dict, Any

class AgentCoordinator:
    async def coordinate_agents(
        self, 
        agents: List[DevelopmentAgent],
        task: Task
    ) -> CoordinationResult:
        """Coordinate multiple agents with proper async handling."""
        
        # Run agents in parallel where possible
        agent_tasks = [
            agent.process_task(task.task_id, task.context)
            for agent in agents
        ]
        
        try:
            # Wait for all agents with timeout
            results = await asyncio.wait_for(
                asyncio.gather(*agent_tasks),
                timeout=300  # 5 minutes
            )
            
            return CoordinationResult(
                success=True,
                agent_results=results
            )
            
        except asyncio.TimeoutError:
            error = self._error_factory.create_timeout_error(
                "Agent coordination timeout",
                {"timeout_seconds": 300, "agent_count": len(agents)}
            )
            raise error
```

### 13. Resource Management

```python
# CORRECT - Proper resource management
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

class AgentLifecycleManager:
    @asynccontextmanager
    async def agent_session(
        self, 
        agent_config: AgentConfig
    ) -> AsyncIterator[ConfiguredAgent]:
        """Manage agent lifecycle with proper cleanup."""
        agent = None
        try:
            # Setup
            agent = await self._create_agent(agent_config)
            await agent.initialize()
            
            yield agent
            
        finally:
            # Cleanup guaranteed
            if agent:
                await agent.cleanup()
                await agent.close_connections()
```

---

## 🚀 DEPLOYMENT RULES

### 14. Configuration Management

```python
# CORRECT - Environment-specific configuration
from pydantic_settings import BaseSettings
from typing import Optional

class AgentSystemSettings(BaseSettings):
    """Agent system configuration with environment variable support."""
    
    # Claude API settings
    claude_api_key: str
    claude_model: str = "claude-3-sonnet-20240229"
    claude_max_tokens: int = 4000
    claude_temperature: float = 0.0
    
    # Agent configuration
    agent_contract_dir: Path = Path("contracts")
    orchestration_timeout: int = 300
    
    # Validation settings
    ltl_verification_enabled: bool = True
    contract_evolution_enabled: bool = False
    
    # Monitoring
    metrics_enabled: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_prefix = "AGENT_SYSTEM_"
        validate_assignment = True
```

### 15. Health Check Standards

```python
# CORRECT - Comprehensive health checks
from typing import Dict, Any
import asyncio

class AgentSystemHealthChecker:
    async def check_health(self) -> HealthCheckResult:
        """Comprehensive system health check."""
        checks = {}
        
        # Check all critical components
        checks["claude_api"] = await self._check_claude_api()
        checks["contract_loading"] = await self._check_contract_loading()
        checks["ltl_verification"] = await self._check_ltl_verification()
        checks["agent_orchestration"] = await self._check_orchestration()
        
        overall_healthy = all(check.healthy for check in checks.values())
        
        return HealthCheckResult(
            healthy=overall_healthy,
            checks=checks,
            timestamp=asyncio.get_event_loop().time()
        )
```

---

## ⚡ ENFORCEMENT AND VALIDATION

### Automated Checks Required

1. **Import Linting**: Detect try/except around imports
2. **Type Checking**: mypy validation with strict settings
3. **Code Formatting**: black and isort compliance
4. **Architecture Validation**: Dependency hierarchy checks
5. **Test Coverage**: Minimum 90% coverage required

### Code Review Checklist

- [ ] No conditional imports
- [ ] All errors use error_handling module
- [ ] **NO untyped data structures or Dict[str, Any] usage**
- [ ] **All metadata and configuration objects fully typed**
- [ ] **ValidationManager used as primary validation interface**
- [ ] **ValidationManager created once at service startup**
- [ ] **Validation contexts passed down through layers (no mid-level creation)**
- [ ] **Info objects and ErrorRecord created only in validation module**
- [ ] **No direct ValidationFactory/ValidationProcess usage**
- [ ] Proper type annotations on all functions
- [ ] Interface-driven design with protocols
- [ ] Object-oriented design with value objects and enums
- [ ] Async/await used correctly
- [ ] Configuration externalized properly
- [ ] Comprehensive logging with structured data
- [ ] Tests follow AAA pattern with descriptive names
- [ ] Documentation includes examples
- [ ] Resource cleanup handled properly

### Violation Consequences

- **Critical Rule Violation** (Import rules, untyped data): **PR automatically rejected**
- **Object-Oriented Rule Violation** (Dict[str, Any], untyped metadata): **Mandatory redesign required**
- **Validation System Rule Violation** (Direct ValidationFactory usage, mid-level ValidationManager creation): **Mandatory redesign required**
- **Architecture Rule Violation**: Mandatory redesign required
- **Code Quality Rule Violation**: PR blocked until fixed
- **Performance Rule Violation**: Performance review required

#### Specific Typing Violations

**Immediate Rejection Triggers:**
- Any use of `Dict[str, Any]` for business data
- Untyped metadata or configuration objects
- Missing type annotations on public interfaces
- Use of `Any` without explicit approval
- Untyped data structures in agent contracts or execution traces

**Zero Tolerance Policy:**
```python
# These patterns will cause IMMEDIATE PR rejection:
metadata = {"key": "value"}                    # ❌ Untyped metadata
def process(data: Dict[str, Any]) -> Any:      # ❌ Untyped interfaces  
config = json.loads(config_string)            # ❌ Untyped JSON parsing
agent_data = response.get("data", {})          # ❌ Untyped external data

# Validation system violations:
factory = ValidationFactory()                 # ❌ Direct ValidationFactory usage
process = ValidationProcess()                  # ❌ Direct ValidationProcess usage
vm = ValidationManager("mid_level")           # ❌ Mid-level ValidationManager creation
bridge = ValidationToErrorContextBridge()     # ❌ Manual bridge handling
```

---

## 🎯 SUCCESS CRITERIA

**Code Quality Gates:**
- All automated checks pass
- Code review approval from 2+ reviewers
- Architecture compliance validated
- Performance benchmarks met
- Documentation complete and accurate

**Implementation Success:**
- Zero conditional imports in production code
- All errors properly handled through error_handling module
- ValidationManager used as single coordination point for all validation
- Info objects and ErrorRecord created only in validation module
- Complete type annotation coverage
- Formal verification capabilities functional
- Contract-driven agent behavior operational

This document serves as the definitive guide for AI agent implementation coding standards. All team members must familiarize themselves with these rules before beginning implementation work.