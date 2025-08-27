# Validation Framework Application Stack Architecture

## Overview

This document defines the proper application stack hierarchy for the validation framework, ensuring consistent usage patterns across all modules and preventing architectural anti-patterns.

## Application Stack Hierarchy

The validation framework follows a strict hierarchical pattern where validation contexts are created at the highest level and flow down through application layers:

```
┌─────────────────────────────────────┐
│ Application/Service Layer (HIGHEST) │  ← ValidationManager creates contexts
├─────────────────────────────────────┤
│ Mid-Level Services                  │  ← Receive and pass contexts down
├─────────────────────────────────────┤
│ Backend/Infrastructure (LOWEST)     │  ← Receive contexts, never create them
└─────────────────────────────────────┘
```

## Core Principles

### 1. ValidationManager at Highest Level

**RULE**: Only the highest application level should create ValidationManager instances.

```python
# ✅ CORRECT: Application/Service Layer
class UserRegistrationService:
    def __init__(self):
        self.validation_manager = ValidationManager("user_registration")
        self.database_manager = DatabaseManager()
    
    def register_user(self, user_data: dict) -> None:
        # Create validation context at highest level
        validation_context = self.validation_manager.get_context()
        
        # Pass context down to mid-level services
        self.database_manager.initialize(database_url, validation_context)
```

### 2. Context Flow Down

**RULE**: Validation contexts flow down through layers and are enriched with operation-specific information.

```python
# ✅ CORRECT: Context flows down through all layers

# Application Layer
validation_manager = ValidationManager("database_operations")
validation_context = validation_manager.get_context()

# Mid Layer
database_manager.initialize(database_url, validation_context)

# Backend Layer  
backend.initialize(database_url, validation_context)
```

### 3. No ValidationFactory at Service Level

**RULE**: Service developers should never use ValidationFactory directly. ValidationManager handles all factory interactions internally.

```python
# ❌ INCORRECT: Direct ValidationFactory usage at service level
from validation.factories.validation_factory import ValidationFactory
factory = ValidationFactory()
context = factory.create_context(descriptor)

# ✅ CORRECT: Use ValidationManager
validation_manager = ValidationManager("service_operation")
validation_context = validation_manager.get_context()
```

### 4. Bridge Pattern for Error Handling

**RULE**: When validation contexts need to be converted to error contexts, always use ValidationToErrorContextBridge.

```python
# ✅ CORRECT: Bridge pattern for error handling
def handle_error(self, validation_context: IValidationContext, message: str):
    bridge = ValidationToErrorContextBridge()
    error_context = bridge.create_error_context_from_validation(validation_context)
    error = error_factory.create_validation_error(message, error_context=error_context)
    error.raise_error()
```

## Architectural Anti-Patterns

### ❌ ANTI-PATTERN: create_minimal() Usage

**REMOVED**: The `create_minimal()` method has been removed from ValidationContext as it violates proper architectural hierarchy.

```python
# ❌ FORBIDDEN: This pattern is now impossible
validation_context = ValidationContext.create_minimal("field.path")
```

**Why it was removed**: Creates validation contexts at wrong architectural level, bypassing proper ValidationManager flow.

### ❌ ANTI-PATTERN: Mid-Level Context Creation

**RULE**: Mid-level services should never create validation contexts.

```python
# ❌ INCORRECT: DatabaseManager creating contexts
class DatabaseManager:
    def initialize(self, database_url: URI) -> None:
        # DON'T DO THIS - wrong architectural level
        validation_context = ValidationManager("database").get_context()
```

```python
# ✅ CORRECT: DatabaseManager receives contexts
class DatabaseManager:
    def initialize(self, database_url: URI, validation_context: IValidationContext) -> None:
        # Store and use the provided context
        self._validation_context = validation_context
```

### ❌ ANTI-PATTERN: Backend Layer Validation Creation

**RULE**: Backend/infrastructure layers should never create validation contexts or ValidationManager instances.

```python
# ❌ INCORRECT: Backend creating validation contexts
class PostgreSQLBackend:
    def initialize(self, database_url: URI) -> None:
        # DON'T DO THIS - wrong architectural level
        validation_manager = ValidationManager("postgresql")
```

```python
# ✅ CORRECT: Backend receives validation contexts
class PostgreSQLBackend:
    def initialize(self, database_url: URI, validation_context: IValidationContext) -> None:
        # Use the provided context from higher level
        self._validation_context = validation_context
```

## Implementation Patterns

### Service Layer Pattern

```python
class ApplicationService:
    """Highest level - creates ValidationManager."""
    
    def __init__(self):
        # Create ValidationManager at application level
        self.validation_manager = ValidationManager("application_service")
        self.database_manager = DatabaseManager()
    
    def perform_operation(self, data: dict) -> None:
        # Get validation context from manager
        validation_context = self.validation_manager.get_context()
        
        # Pass context to lower levels
        self.database_manager.initialize(self.config.database_url, validation_context)
        
        # Use validation manager for operation validation
        result = self.validation_manager.validate(data)
        if not result.is_valid():
            # ValidationManager handles error conversion automatically
            pass
```

### Mid-Level Service Pattern

```python
class DatabaseManager:
    """Mid-level - receives and stores validation context."""
    
    def __init__(self):
        self._validation_context: Optional[IValidationContext] = None
        self._backends: dict = {}
    
    def initialize(self, database_url: URI, validation_context: IValidationContext) -> None:
        # Store validation context for subsequent operations
        self._validation_context = validation_context
        
        # Pass context down to backends
        backend = PostgreSQLBackend()
        backend.initialize(database_url, validation_context)
        self._backends['postgresql'] = backend
    
    def get_session(self) -> Session:
        if not self._validation_context:
            raise ValueError("DatabaseManager not initialized")
        
        # Create child context for specific operations
        session_context = self._validation_context.create_child("session")
        
        try:
            return self._backends['postgresql'].get_session()
        except Exception as e:
            # Use bridge pattern for error handling
            bridge = ValidationToErrorContextBridge()
            error_context = bridge.create_error_context_from_validation(session_context)
            error = error_factory.create_validation_error(f"Session error: {e}", error_context=error_context)
            error.raise_error()
```

### Backend Layer Pattern

```python
class PostgreSQLBackend:
    """Backend level - receives validation context, never creates."""
    
    def __init__(self):
        self._validation_context: Optional[IValidationContext] = None
    
    def initialize(self, database_url: URI, validation_context: IValidationContext) -> None:
        # Store the validation context provided by higher level
        self._validation_context = validation_context
        
        try:
            self._engine = create_async_engine(str(database_url))
        except Exception as e:
            # Use bridge pattern for error handling with provided context
            bridge = ValidationToErrorContextBridge()
            error_context = bridge.create_error_context_from_validation(validation_context)
            error = error_factory.create_validation_error(f"Backend initialization failed: {e}", error_context=error_context)
            error.raise_error()
```

## Validation Context Lifecycle

### 1. Creation (Application Layer)
```python
# Application layer creates ValidationManager
validation_manager = ValidationManager("user_operations")
validation_context = validation_manager.get_context()
```

### 2. Flow Down (Through Layers)
```python
# Context flows down, gets enriched at each level
service_layer.process(data, validation_context)
  ↓
database_manager.initialize(config, validation_context)  
  ↓
backend.initialize(database_url, validation_context)
```

### 3. Child Context Creation (Operation-Specific)
```python
# Lower levels can create child contexts for specific operations
session_context = validation_context.create_child("session")
transaction_context = validation_context.create_child("transaction")
```

### 4. Error Handling (Bridge Pattern)
```python
# Convert validation context to error context when needed
bridge = ValidationToErrorContextBridge()
error_context = bridge.create_error_context_from_validation(validation_context)
error = error_factory.create_validation_error(message, error_context=error_context)
error.raise_error()
```

## Summary

This architectural pattern ensures:

1. **Clear Separation of Concerns**: Each layer has well-defined responsibilities
2. **Proper Context Flow**: ValidationContext flows down and gets enriched
3. **Single Source of Truth**: ValidationManager is the only entry point for validation
4. **Consistent Error Handling**: Bridge pattern provides uniform error conversion
5. **No Architectural Shortcuts**: Eliminates anti-patterns like `create_minimal()`

Following this architecture prevents the need to repeatedly explain validation framework patterns and ensures consistent implementation across all modules.