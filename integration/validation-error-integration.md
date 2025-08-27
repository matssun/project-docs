# Validation-Error Integration Architecture

## Overview

This document describes the **interface-only integration architecture** between the validation and error handling modules, ensuring clean separation of concerns and maintainable dependencies.

## Architectural Principles

### Single Responsibility
- **Validation Module**: Owns Info object creation and lifecycle
- **Error Handling Module**: Consumes Info objects through interfaces only
- **Bridge Pattern**: Coordinates conversion using interface contracts

### Interface-Only Dependencies
- **No concrete types** cross module boundaries
- **All interactions** through well-defined interface contracts
- **Clean separation** prevents circular dependencies and tight coupling

### Information Flow Direction
```
ValidationContext → Bridge → InfoContainer → ErrorContext → ErrorState
(validation)      (bridge)  (interfaces)   (error)      (error)
```

## Component Integration

### 1. ValidationContext (Validation Module)
**Purpose**: Rich validation state container with comprehensive information

**Responsibilities**:
- Contains `ValidationState` with validation progress and results
- Holds `ValidationDescriptor` with validation rules and configuration
- Provides event coordination for validation lifecycle
- Maintains validation hierarchy through parent/child relationships

**Interface Exports**: `IValidationContext`

### 2. InfoFactory (Validation Module)
**Purpose**: Extract typed information objects from ValidationContext

**Responsibilities**:
- Extract all available info types from validation context
- Create concrete Info objects (ValidationInfo, SecurityInfo, etc.)
- Transform validation state into structured information objects
- Handle graceful degradation when information is unavailable

**Key Methods**:
```python
InfoFactory.extract_validation_info_from_context(context)
InfoFactory.extract_schema_info_from_context(context)
InfoFactory.extract_security_info_from_context(context)
InfoFactory.extract_xml_validation_info_from_context(context)
InfoFactory.extract_configuration_info_from_context(context)
InfoFactory.extract_operational_info_from_context(context)
```

### 3. InfoContainer (Validation Module)
**Purpose**: Unified container for all Info objects with interface boundary

**Responsibilities**:
- Hold concrete Info objects internally
- Provide interface access (`IInfoContainer`) to other modules
- Support unified summary generation (`get_summary()`)
- Enable structured access to all information types

**Interface Properties**:
```python
validation_info: Optional[IValidationInfo]
schema_info: Optional[ISchemaInfo]
security_info: Optional[ISecurityInfo]
network_info: Optional[INetworkInfo]
configuration_info: Optional[IConfigurationInfo]
operational_info: Optional[IOperationalInfo]
error_details_info: Optional[IErrorDetailsInfo]
```

### 4. ValidationToErrorContextBridge (Validation Module)
**Purpose**: Single conversion point between validation and error contexts

**Responsibilities**:
- Extract Info objects using InfoFactory
- Populate InfoContainer with extracted information
- Create ErrorContext with populated InfoContainer
- Maintain interface boundaries during conversion

**Key Method**:
```python
def create_error_context_from_validation(
    self, validation_context: IValidationContext
) -> IErrorContext:
    # Extract all available info
    info_container = InfoContainer()
    info_container.validation_info = InfoFactory.extract_validation_info_from_context(context)
    info_container.schema_info = InfoFactory.extract_schema_info_from_context(context)
    # ... extract other info types
    
    # Create ErrorContext with interface boundary
    return ErrorContext(
        field_path=extracted_field_path,
        error_code=ErrorCode.VALIDATION_FAILED,
        category=ErrorCategory.VALIDATION,
        severity=determined_severity,
        info_container=info_container,  # Interface only
    )
```

### 5. ErrorContext (Error Handling Module)
**Purpose**: Error-specific context with interface-only dependencies

**Responsibilities**:
- Receive pre-populated `IInfoContainer` from bridge
- Extract individual info interfaces for ErrorState
- Create minimal `IErrorInfo` when ErrorState not provided
- Maintain error hierarchy through parent/child relationships

**Interface Dependencies**:
```python
def __init__(
    self,
    field_path: FieldPath,
    error_code: ErrorCode,
    category: ErrorCategory,
    severity: ErrorSeverity,
    info_container: IInfoContainer,  # Interface only
    *,
    error_state: Optional[IErrorState] = None,
) -> None:
    # Extract interfaces for ErrorState
    error_state = ErrorState(
        error_info=_MinimalErrorInfo(...),  # Internal implementation
        schema_info=info_container.schema_info,  # Interface
        security_info=info_container.security_info,  # Interface
        # ... other interfaces
    )
```

### 6. ErrorState (Error Handling Module)
**Purpose**: Typed error state with interface-only properties

**Responsibilities**:
- Store individual Info interfaces as typed properties
- Provide error state management (phases, hierarchy)
- Generate comprehensive error summaries
- Support error state evolution and child creation

**Interface Properties**:
```python
error_info: IErrorInfo  # Required core error information
schema_info: Optional[ISchemaInfo]  # Optional typed interfaces
security_info: Optional[ISecurityInfo]
network_info: Optional[INetworkInfo]
configuration_info: Optional[IConfigurationInfo]
operational_info: Optional[IOperationalInfo]
```

## Integration Flow

### Complete Validation-to-Error Scenario

```python
# 1. Validation detects failure with rich context
validation_manager = ValidationManager("user_registration")
validation_context = validation_manager.get_current_context()

# 2. Bridge converts validation context to error context
bridge = ValidationToErrorContextBridge()
error_context = bridge.create_error_context_from_validation(validation_context)

# 3. Error factory creates error with rich information
error_factory = get_error_factory()
error = error_factory.create_validation_error(
    message="Email validation failed: invalid format",
    error_context=error_context  # Contains all validation info as interfaces
)

# 4. Error is raised with complete contextual information
error.raise_error()
```

### Information Enrichment Process

1. **Validation State Capture**:
   - ValidationContext contains rich validation state
   - ValidationDescriptor defines validation rules and constraints
   - ValidationResult contains outcomes and issues

2. **Information Extraction**:
   - InfoFactory extracts all relevant information types
   - Each extraction method handles missing data gracefully
   - Concrete Info objects created with structured data

3. **Container Population**:
   - InfoContainer holds all extracted Info objects
   - Container provides unified interface boundary
   - All information accessible through typed properties

4. **Interface Transfer**:
   - Bridge passes InfoContainer as IInfoContainer interface
   - Error handling receives interface reference only
   - No concrete validation dependencies in error handling

5. **Error State Creation**:
   - ErrorContext extracts individual interfaces from container
   - ErrorState receives typed interface properties
   - Complete error context available for strategies and formatting

## Benefits

### Clean Architecture
- **Separation of concerns**: Each module has single responsibility
- **Interface boundaries**: Clean contracts prevent tight coupling
- **Dependency direction**: Validation → Error (no reverse dependencies)

### Rich Information Transfer
- **Comprehensive context**: All validation information preserved
- **Typed access**: Strongly typed interfaces for all data
- **Graceful degradation**: Missing info doesn't break error handling

### Maintainable Design
- **Centralized creation**: Info objects managed in one place
- **Interface stability**: Implementation changes don't affect consumers
- **Testable components**: Easy mocking through interface contracts

## Critical Rules

### For Validation Module
- **OWN** all Info object creation and lifecycle
- **USE** InfoFactory to extract information from contexts
- **POPULATE** InfoContainer with concrete implementations
- **PROVIDE** InfoContainer as IInfoContainer interface to other modules

### For Error Handling Module
- **RECEIVE** IInfoContainer interface from validation via bridge
- **EXTRACT** individual info interfaces from container
- **CONSUME** information through interface contracts only
- **NEVER** create Info objects or import validation concrete types

### For Integration Points
- **ALWAYS** use ValidationToErrorContextBridge for conversion
- **NEVER** create ErrorContext directly from ValidationContext
- **MAINTAIN** interface boundaries during all transfers
- **HANDLE** missing information gracefully at all levels

This architecture ensures **clean separation**, **rich information transfer**, and **maintainable integration** between validation and error handling concerns while preserving all contextual information needed for comprehensive error reporting.