# Validator Refactoring Guide

## Overview

This guide documents the standard pattern for refactoring validators to eliminate anti-patterns and follow proper factory usage, error handling, and type safety.

## Key Changes Required

### 1. **Constructor Changes**

**BEFORE:**

```python
def __init__(self, validation_result_builder_factory: IValidationResultBuilderFactory = None) -> None:
    self._validation_result_builder_factory = validation_result_builder_factory or ValidationResultBuilderFactory()
```

**AFTER:**

```python
def __init__(
    self,
    validation_context_factory: IValidationContextFactory,
    timer: IGenericTimer,
    validation_result_builder_factory: Optional[IValidationResultBuilderFactory] = None,
) -> None:
    self._validation_context_factory = validation_context_factory
    self._timer = timer
    self._validation_result_builder_factory = validation_result_builder_factory or ValidationResultBuilderFactory()
```

### 2. **Eliminate BasicTimer Anti-Pattern**

**BEFORE:**

```python
class BasicTimer:
    def start(self): pass
    def stop(self): pass
    def elapsed(self): return 0.0

descriptor = ValidationDescriptor(
    validation_type=ValidationType.RESPONSE,
    field_path="response",
    timing_info=BasicTimer(),
)
```

**AFTER:**

```python
# Use injected timer
timing_info=self._timer
```

### 3. **Replace Direct ValidationContext Creation**

**BEFORE:**

```python
validation_context = ValidationContext(
    field_path="response",
    validation_type=ValidationType.RESPONSE,
    validation_state=ValidationState(
        validation_descriptor=descriptor,
        phase="response_validation"
    ),
)
```

**AFTER:**

```python
# For RequestValidator
validation_context = self._validation_context_factory.create_request_validation_context(
    field_path=FieldPath("request"),
    request_type=request_type,
    timing_info=self._timer,
    validation_mode=ValidationMode.STRICT,
    parent_context=None,
)

# For ResponseValidator
validation_context = self._validation_context_factory.create_response_validation_context(
    field_path=FieldPath("response"),
    response_type=response_type,
    timing_info=self._timer,
    validation_mode=ValidationMode.STRICT,
    parent_context=None,
)

# For XMLValidator
validation_context = self._validation_context_factory.create_xml_validation_context(
    field_path=FieldPath("xml"),
    xml_type=xml_type,
    namespace=namespace,
    root_element=root_element,
    timing_info=self._timer,
    validation_method=XMLValidationMethod.SCHEMA,
    parent_context=None,
)
```

### 4. **Handle Immutable Descriptors Correctly**

**BEFORE:**

```python
# This is WRONG - descriptors are immutable
validation_context.get_validation_state().set_response_type(response_type)
```

**AFTER:**

```python
# Get type information BEFORE creating context
response_type = response.__class__.__name__ if hasattr(response, "__class__") else "unknown"

# Pass type information during context creation
validation_context = self._validation_context_factory.create_response_validation_context(
    field_path=FieldPath("response"),
    response_type=response_type,  # Set during creation
    timing_info=self._timer,
    validation_mode=ValidationMode.STRICT,
    parent_context=None,
)
```

### 5. **Use Proper Error Raising Pattern**

**BEFORE:**

```python
validation_error = handle_validation_exception(
    validation_context=validation_context,
    error=e,
    validation_stage="response_validation",
    response_type=response_type,
)
raise validation_error  # WRONG
```

**AFTER:**

```python
validation_error = handle_validation_exception(
    validation_context=validation_context,
    error=e,
    validation_stage="response_validation",
    response_type=response_type,
)
validation_error.raise_error()  # CORRECT
```

### 6. **Required Imports**

Add these imports to all validators:

```python
from core_interfaces.common.common import FieldPath
from core_interfaces.common.validation_types import ValidationMode
from core_interfaces.interfaces.factories.ivalidation_context_factory import (
    IValidationContextFactory,
)
from core_interfaces.interfaces.timers.itimer import IGenericTimer
```

## Validator-Specific Factory Methods

### RequestValidator

```python
self._validation_context_factory.create_request_validation_context(
    field_path=FieldPath("request"),
    request_type=request.__class__.__name__,
    timing_info=self._timer,
    validation_mode=ValidationMode.STRICT,
    parent_context=None,
)
```

### ResponseValidator

```python
self._validation_context_factory.create_response_validation_context(
    field_path=FieldPath("response"),
    response_type=response.__class__.__name__,
    timing_info=self._timer,
    validation_mode=ValidationMode.STRICT,
    parent_context=None,
)
```

### XMLValidator

```python
self._validation_context_factory.create_xml_validation_context(
    field_path=FieldPath("xml"),
    xml_type=XMLType.DOCUMENT,
    namespace=namespace,
    root_element=root_element,
    timing_info=self._timer,
    validation_method=XMLValidationMethod.SCHEMA,
    parent_context=None,
)
```

### SchemaValidator

```python
self._validation_context_factory.create_schema_validation_context(
    field_path=FieldPath("schema"),
    schema_type=SchemaType.XSD,
    schema_version=version,
    timing_info=self._timer,
    validation_mode=ValidationMode.STRICT,
    schema_location=schema_location,
    parent_context=None,
)
```

## Common Mistakes to Avoid

1. **Don't try to modify immutable descriptors** - Set all information during context creation
2. **Don't use `raise validation_error`** - Use `validation_error.raise_error()` instead
3. **Don't create inline `BasicTimer` classes** - Use the injected timer
4. **Don't use `**kwargs` in constructor** - Use explicit typed parameters
5. **Don't access data with `hasattr`/`getattr`/`setattr`** - Use typed object access only
6. **Don't use metadata dictionaries** - Use typed descriptor objects

## Testing Pattern

When creating validators in tests, inject the required dependencies:

```python
# In tests
mock_factory = Mock(spec=IValidationContextFactory)
mock_timer = Mock(spec=IGenericTimer)

validator = ResponseValidator(
    validation_context_factory=mock_factory,
    timer=mock_timer,
    validation_result_builder_factory=None,
)
```

## Implementation Order

1. Update constructor to inject dependencies
2. Replace all BasicTimer anti-patterns
3. Replace direct ValidationContext creation with factory calls
4. Fix immutable descriptor handling
5. Update error raising pattern
6. Add required imports
7. Update tests to provide required dependencies

This pattern ensures type safety, proper factory usage, and consistent error handling across all validators.
