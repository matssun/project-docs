# Validation Context/State/Descriptor Refactoring Plan

## Core Design Decisions

### 1. Factory-Only Creation Pattern

- **All ValidationContext creation must go through ValidationContextFactory**
- Multiple typed factory methods: `create_request_validation_context()`, `create_xml_validation_context()`, etc.
- No direct ValidationContext constructor calls
- Eliminates BasicTimer anti-patterns and enforces proper descriptor creation

### 2. Immutable ValidationDescriptor

- ValidationDescriptor is immutable after construction
- Must be provided during ValidationState creation
- `set_validation_descriptor()` method removed from interfaces
- ValidationState validates descriptor is not None in `__post_init__()`

### 3. Child Context Creation Strategy

- **Manual attachment pattern**: Create child via f actory + attach separately
- Standard factory methods used for all contexts (no special child methods)
- `attach_child(parent_context, child_context)` method handles hierarchy
- Field paths handled normally - no automatic "parent." prefixing

### 4. Timing/Monitoring Removed

- All timing and monitoring moved to external event system
- Remove timing_info from descriptors and contexts
- ValidationContext emits events for external coordination

### 5. Validation Event Scope

- **Per-Context Events**: Each context emits own start/end validation events
- Individual contexts are independently controllable
- External monitoring correlates events using parent-child relationships
- Matches current usage patterns in codebase

## Child Context Creation Pattern

### Current Problem

- `create_child()` methods bypass factory enforcement
- Child contexts can be completely different validation types than parents
- No way to ensure immutable attributes are properly set

### Solution

Instead of: `child = parent.create_child("field_name")`
Use:

```
child = factory.create_xml_validation_context(field_path="parent.field.xml", ...)
factory.attach_child(parent, child)
```

## Descriptor Purpose Clarification

- Descriptors are **validation state containers** describing the validation process
- Different descriptor types avoid needing separate State classes for each validation type
- Contains validation rules and constraints, not location information
- `create_child_descriptor()` exists because descriptors are immutable and contain field_path

## Implementation Priority

1. Update IValidationState and ValidationState interfaces (completed)
2. Design factory interfaces for child creation and attachment
3. Remove timing/monitoring from validation core
4. Update validators to use factory pattern
5. Remove BasicTimer anti-patterns

## Key Interface Requirements

- `IValidationContextFactory` with typed creation methods
- `attach_child(parent, child)` method with business rule enforcement
- Remove `set_validation_descriptor()` from IValidationState
- Per-context validation lifecycle events

## Current Usage Analysis

- Request/Response validators use start/end for phase tracking
- Request factories create child contexts for parameter validation
- Users don't manually track entire context hierarchies
- External monitoring service correlates events via parent-child relationships
- Per-context events match existing usage patterns
