# Validation Error Handling Refactoring Plan

## Objective

Standardize all validation error creation to use Level 3 convenience functions from `validation.integrations.error_handling_integration`, eliminating direct factory usage and ensuring consistent error handling across the system.

## Current Architecture Issues

- Mixed error creation patterns (Level 1, 2, and 3)
- Unused `ValidationResultAdapter` class
- Inconsistent error handling across validators
- Direct factory calls bypass unified pipeline

## Target Architecture

All validation errors should use convenience functions:

- `create_validation_error_from_context()`
- `handle_validation_exception()`

## Files and Classes Requiring Refactoring

### Phase 1: Core Validators

**File**: `validation/src/validation/validators/request_validator.py`

- **Class**: `RequestValidator`
- **Methods**: `validate()`, `validate_structure()`, `validate_params()`

**File**: `validation/src/validation/validators/response_validator.py`

- **Class**: `ResponseValidator`
- **Methods**: `validate()`, validation methods

**File**: `validation/src/validation/validators/validator.py`

- **Class**: `Validator` (base class)
- **Methods**: Any error creation methods

### Phase 2: XML Validation System

**File**: `validation/src/validation/validators/xml/xml_validator.py`

- **Class**: `XMLValidator`
- **Methods**: `extract_schema_based_data()`, validation methods

**File**: `validation/src/validation/validators/xml/xml_schema_registry.py`

- **Class**: `XMLSchemaRegistry`
- **Methods**: Schema validation methods

**File**: `validation/src/validation/validators/xml/xml_validation_handling.py`

- **Class**: `XMLValidationContextManager`
- **Methods**: `__enter__()`, `__exit__()`

### Phase 3: Constraint System

**File**: `validation/src/validation/constraints/constraint_registry.py`

- **Class**: `ConstraintRegistry`
- **Methods**: `_raise_config_error()`, constraint creation methods

### Phase 4: Utility Classes

**File**: `validation/src/validation/utils/message_templates.py`

- **Class**: `MessageTemplateManager`
- **Methods**: `generate_validation_specific_message()`

## Files to Remove

### Complete Removal

**File**: `validation/src/validation/adapters/validation_adapter.py`

- **Class**: `ValidationResultAdapter` (unused/deprecated)

### Partial Changes

**File**: `validation/src/validation/adapters/__init__.py`

- Remove `ValidationResultAdapter` export

**File**: `validation/src/validation/__init__.py`

- Remove `ValidationResultAdapter` from exports

## Required Import Changes

### Add to All Refactored Files

```python
from validation.integrations.error_handling_integration import (
    create_validation_error_from_context,
    handle_validation_exception
)
```

### Remove from Refactored Files

```python
from error_handling import ValidationError, get_error_factory
```

## Implementation Strategy

### Phase 1: Core Validators (Priority: High)

1. Refactor `RequestValidator` and `ResponseValidator`
2. Update base `Validator` class
3. Run tests to ensure functionality

### Phase 2: XML System (Priority: Medium)

1. Refactor XML validators
2. Update XML context managers
3. Test XML validation workflows

### Phase 3: Constraint System (Priority: Medium)

1. Refactor constraint registry
2. Update constraint error handling
3. Test constraint validation

### Phase 4: Cleanup (Priority: Low)

1. Remove unused `ValidationResultAdapter`
2. Update package exports
3. Clean up imports
4. Run full test suite

## Success Criteria

- All validation errors use convenience functions
- No direct `error_factory` calls in validation code
- `ValidationResultAdapter` removed
- All tests pass
- Consistent error handling patterns

## Risk Mitigation

- Implement phase by phase
- Run tests after each phase
- Keep rollback capability
- Monitor error handling consistency

## Testing Requirements

- Unit tests for each refactored class
- Integration tests for error workflows
- Verify error context bridging works correctly
- Confirm error message consistency
