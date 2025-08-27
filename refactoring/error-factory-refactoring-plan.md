# Error Factory Refactoring Plan

## Objective

Eliminate Info objects and parameter shuffling by consolidating all extraction logic directly into ErrorFactory. Achieve optimal performance by passing ValidationContext directly to ErrorFactory.

## Core Principles

- **FORBIDDEN**: Untyped dictionaries (`Dict[str, Any]`) or metadata constructs
- **REQUIRED**: Strongly typed objects using ValidationDescriptors and ValidationContext
- **GOAL**: Direct ValidationContext → ErrorFactory flow with internal extraction

## Phase 1: Interface Layer Refactoring

### 1.1 Update IErrorFactory Interface

**Task**: Replace Info object parameters with ValidationContext parameters

**Changes Required**:

- Remove all `*_info: IInfo` parameters from method signatures
- Add `validation_context: IValidationContext` as primary parameter
- Keep message, error_context, and is_retryable parameters
- Document that extraction logic moves to implementation

**New Signature Pattern**:

```python
def create_validation_error(
    self,
    message: str,
    error_context: IErrorContext,
    validation_context: IValidationContext,
    is_retryable: bool = False,
) -> IValidationError
```

**Documentation Required**:

- Inline docstring: "Extracts all validation information directly from ValidationContext using strongly typed ValidationDescriptor"
- Inline docstring: "No Info objects or metadata dictionaries - uses typed descriptor properties only"

### 1.2 Remove Multi-Tier API Support

**Task**: Eliminate Tier 1 (legacy params) and Tier 2 (Info objects) from interfaces

**Changes Required**:

- Remove all individual parameter variants (validation_rule, expected_type, etc.)
- Remove all Info object parameters
- Keep only ValidationContext-based API (current Tier 3)
- Update all interface docstrings to reflect single-tier design

### 1.3 Update Error Interfaces

**Task**: Ensure error interfaces can accept ValidationDescriptor directly

**Changes Required**:

- Update IValidationError, ISchemaValidationError, etc. to store ValidationDescriptor
- Remove Info object storage from error interfaces
- Add validation_descriptor property to error interfaces
- Document: "Stores immutable ValidationDescriptor reference for type-safe access"

## Phase 2: Implementation Layer Refactoring

### 2.1 Refactor ErrorFactory Implementation

**Task**: Consolidate all extraction logic into ErrorFactory methods

**Changes Required**:

- Remove InfoContainer usage entirely
- Remove InfoConversionUtils dependencies
- Implement direct ValidationContext property extraction
- Use isinstance checks for ValidationDescriptor type determination

**Extraction Logic Pattern**:

```python
def _extract_from_validation_context(self, validation_context: IValidationContext):
    descriptor = validation_context.validation_state.validation_descriptor
    field_path = validation_context.field_path
    validation_rule = validation_context.validation_rule
    
    # Type-safe extraction using isinstance
    if isinstance(descriptor, ISchemaValidationDescriptor):
        # Extract schema-specific properties
    elif isinstance(descriptor, IXMLValidationDescriptor):
        # Extract XML-specific properties
    # etc.
```

**Documentation Required**:

- Inline comment: "Direct property access - no metadata dictionaries used"
- Inline comment: "Type-safe extraction using ValidationDescriptor interfaces"

### 2.2 Update Error Constructors

**Task**: Modify error classes to accept ValidationDescriptor directly

**Changes Required**:

- Replace InfoContainer parameters with ValidationDescriptor parameters
- Remove Info object storage fields
- Store ValidationDescriptor reference directly
- Update `_create` methods to use ValidationDescriptor

**Constructor Pattern**:

```python
def __init__(
    self,
    message: str,
    error_context: IErrorContext,
    validation_descriptor: IValidationDescriptor,
    is_retryable: bool = False,
):
    self.validation_descriptor = validation_descriptor  # Direct storage
    # Extract properties on-demand using isinstance checks
```

### 2.3 Eliminate Supporting Classes

**Task**: Remove classes that become obsolete

**Classes to Remove**:

- InfoContainer
- InfoConversionUtils
- All Info implementations (ValidationInfo, SchemaInfo, etc.)
- InfoFactory (keep only if used elsewhere)

**Verification Required**:

- Ensure no references remain in codebase
- Update imports throughout codebase
- Remove from **init**.py exports

### 2.4 Update ValidationToErrorContextBridge

**Task**: Simplify bridge to direct ErrorFactory calls

**Changes Required**:

- Remove InfoFactory usage
- Remove Info object creation
- Pass ValidationContext directly to ErrorFactory
- Document: "Bridge now provides direct ValidationContext pass-through"

## Phase 3: Verification and Testing

### 3.1 Type Safety Verification

**Checklist**:

- [ ] No Dict[str, Any] usage anywhere in error creation
- [ ] No metadata dictionary access
- [ ] All property access through typed interfaces
- [ ] isinstance checks used for type determination

### 3.2 Performance Verification

**Metrics to Measure**:

- Error creation time (should decrease)
- Memory allocation (should decrease)
- Object creation count (should decrease)

### 3.3 Functionality Verification

**Test Coverage Required**:

- All ValidationDescriptor types work correctly
- Error context creation maintains all data
- No information loss during refactoring

## Implementation Order

### Step 1: Interface Updates

1. Update IErrorFactory interface signatures
2. Update error interfaces to accept ValidationDescriptor
3. Ensure all interface changes compile

### Step 2: Implementation Updates

1. Update ErrorFactory implementation with extraction logic
2. Update error class constructors
3. Test individual error creation works

### Step 3: Clean Up

1. Remove InfoContainer and InfoConversionUtils
2. Update ValidationToErrorContextBridge
3. Remove unused imports and classes

### Step 4: Verification

1. Run full test suite
2. Verify no Dict[str, Any] usage
3. Measure performance improvements

## Success Criteria

- [ ] ValidationContext passed directly to ErrorFactory
- [ ] All extraction logic consolidated in ErrorFactory
- [ ] Zero Info object creation
- [ ] Zero metadata dictionary usage
- [ ] Zero parameter shuffling between layers
- [ ] Strongly typed property access only
- [ ] Performance improvement measurable
- [ ] All existing functionality preserved

## Risk Mitigation

### Backward Compatibility

- Update all calling code simultaneously
- Ensure comprehensive test coverage before changes

### Type Safety

- Use isinstance checks consistently
- Document all property access patterns
- Verify no Any types introduced

### Performance

- Measure before/after performance
- Monitor memory allocation patterns
- Ensure no regression in error handling speed
