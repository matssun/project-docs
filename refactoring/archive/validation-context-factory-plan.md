# Validation Context Factory Unification Plan

## Problem Statement

Current validation system has too many factories with overlapping responsibilities and relies heavily on Optional types, leading to defensive programming and unclear object lifecycles.

## Core Decisions

### 1. Eliminate Optional Types in Core Interfaces

- `IValidationState.validation_descriptor` becomes **required** (not Optional)
- `IValidationState.validation_process` becomes **required** (not Optional)
- `IValidationState.validation_result` remains Optional (only set after validation completes)

### 2. Create Unified ValidationContextFactory

- **Replace** multiple context creation paths with single authoritative factory
- **Consolidate** ValidatorFactory context creation methods into this factory
- **Preserve** other specialized factories (ProcessTracker, ResultBuilder) for their focused purposes
- Factory methods create complete object graphs with guaranteed non-Optional components

### 3. Enforce Type Safety in Parent-Child Contexts

- Parent contexts with `IRequestValidationDescriptor` can only create children with `IRequestValidationDescriptor`
- Child creation delegates descriptor cloning to parent descriptor
- Context manages hierarchy and relationships, descriptor manages domain-specific inheritance

## Implementation Guidance

### Factory Design

- Create type-specific factory methods: `create_request_validation_context()`, `create_xml_validation_context()`, etc.
- Each method returns context with guaranteed descriptor type and initialized process
- Factory ensures all required components exist at creation time

### Parent-Child Context Pattern

- **Keep existing** `create_child()` method signature
- **Add** `create_child_descriptor()` method to each descriptor type
- Context calls descriptor's child creation method, then builds child context
- Maintain existing parent-child relationship and inheritance patterns

### Interface Updates

- Update `IValidationState` to remove Optional from `validation_descriptor` and `validation_process`
- Add `create_child_descriptor(field_name: str) -> Self` method to all descriptor interfaces
- Ensure ValidationState constructor requires descriptor and process parameters

### Factories to be Deprecated

- **ValidatorFactory.create_request_context()** - replaced by ValidationContextFactory
- **ValidatorFactory.create_response_context()** - replaced by ValidationContextFactory
- **ValidatorFactory.create_validator_with_context()** - context creation part replaced
- **State factory methods** (referenced in tests) - ValidationState now has single constructor
- **EnhancedValidatorFactory context creation methods** - consolidated into unified factory

### Factories to be Preserved

- **ValidationProcessTrackerFactory** - for advanced process tracking
- **ValidationResultBuilderFactory** - for complex result aggregation  
- **ValidationObjectFactory** - for typed validation objects
- **ServiceFactoryAdapter** - for service-specific needs
- **ConnectionPoolFactoryAdapter** - for connection management

### Migration Strategy

- Phase 1: Create unified ValidationContextFactory alongside existing factories
- Phase 2: Update interface definitions to remove Optional types
- Phase 3: Migrate existing code to use unified factory
- Phase 4: Remove deprecated factory methods and mark classes as deprecated

### Benefits

- **Eliminates defensive programming** - no more Optional checking
- **Reduces factory complexity** - clear ownership of responsibilities
- **Maintains type safety** - parent-child contexts preserve descriptor types
- **Simplifies validation workflows** - guaranteed object availability
- **Preserves existing patterns** - parent-child context hierarchy unchanged

### Factory Responsibilities After Changes

| Factory                             | Responsibility                                  |
| ----------------------------------- | ----------------------------------------------- |
| **ValidationContextFactory**        | Complete context creation with guaranteed types |
| **ValidationProcessTrackerFactory** | Advanced process tracking and operations        |
| **ValidationResultBuilderFactory**  | Complex result aggregation                      |
| **ValidationObjectFactory**         | Typed validation objects                        |

### Success Criteria

- Zero Optional checking in validation workflows
- Single entry point for context creation
- Type-safe parent-child context inheritance
- Reduced factory count while maintaining clear separation of concerns
