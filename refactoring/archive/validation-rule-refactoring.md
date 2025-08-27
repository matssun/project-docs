# Validation Rule Refactoring Plan

## Executive Summary

This document outlines the refactoring plan to establish a single source of truth for validation rule information by splitting the current `IActiveRule` into two distinct interfaces: `IValidationRule` (immutable) and `IValidationRuleStatus` (mutable).

## 🚨 CRITICAL REQUIREMENT: STRONGLY TYPED OBJECTS ONLY

**FORBIDDEN**: All untyped dictionaries, metadata structures, and `Dict[str, Any]` patterns are strictly prohibited. This refactoring enforces strongly typed object-oriented design throughout.

## Current Problems Identified

### Single Source of Truth Violations

- `ValidationContext.validation_rule: IActiveRule` (new approach)
- `ValueValidationDescriptor.validation_rule: str` (legacy - REMOVE)
- Field path and validation type duplicated across multiple locations

### Architecture Issues

- Mixed mutable and immutable concerns in single interface
- Heavy object serialization for events and error handling
- Circular dependencies in error objects

## Storage Locations

### ValidationDescriptor (Immutable Layer)

**CHANGE:** Replace `validation_rule: str` with `validation_rule: IValidationRule`

**Affected Descriptors:**

- `ValueValidationDescriptor` - Remove string `validation_rule` field
- `XMLValidationDescriptor` - Add `validation_rule: IValidationRule`
- `SecurityValidationDescriptor` - Add `validation_rule: IValidationRule`
- `SchemaValidationDescriptor` - Add `validation_rule: IValidationRule`

### ValidationContext (Mutable Layer)  

**CHANGE:** Replace `validation_rule: IActiveRule` with `rule_status: IValidationRuleStatus`

**Updated Properties:**

- `validation_state: IValidationState`
- `rule_status: IValidationRuleStatus` (NEW)
- `parent_context: Optional[IValidationContext]`
- `child_contexts: List[IValidationContext]`
- `event_publisher: Optional[IEventPublisher]`

**Convenience Properties** (derived from rule_status):

- `field_path -> rule_status.rule.field_path`
- `validation_type -> rule_status.rule.rule_type`

## Implementation Strategy

### Phase 1: Create New Interfaces

1. Define `IValidationRule` interface with immutable properties
2. Define `IValidationRuleStatus` interface with mutable properties  
3. Create concrete implementations: `ValidationRule` and `ValidationRuleStatus`
4. Update `RuleStatus` enum if needed for new states

### Phase 2: Update Descriptor Layer

1. Remove `validation_rule: str` from `ValueValidationDescriptor`
2. Add `validation_rule: IValidationRule` to all descriptor types
3. Update `IValidationDescriptor` base interface
4. Ensure descriptor constructors require `IValidationRule`

### Phase 3: Update Context Layer  

1. Replace `validation_rule: IActiveRule` with `rule_status: IValidationRuleStatus` in `ValidationContext`
2. Update `IValidationContext` interface
3. Update convenience property implementations
4. Ensure context constructors require `IValidationRuleStatus`

### Phase 4: Update Factories

1. Modify `ValidationContextFactory` to create both rule and status objects
2. Update factory methods to accept rule parameters and create `IValidationRule`
3. Create `IValidationRuleStatus` with rule reference
4. Ensure atomic creation of context with both components

### Phase 5: Update Usage Patterns

1. **Error Handling:** Update error factories to extract data from `context.rule_status`
2. **Event Transmission:** Use `rule_status.to_json()` for event payloads
3. **Monitoring:** Access rule data through `context.rule_status.rule`
4. **Logging:** Extract structured data from rule status object

### Phase 6: Migration and Cleanup

1. Update all existing callers to use new property paths
2. Remove legacy `IActiveRule` interface
3. Remove string-based validation rule storage
4. Update tests to use new object structure
5. Validate no untyped dictionaries remain

## Use Case Implementations

### Error Handling Pattern

Error factories access rule information through validation context:

**Process:**

1. Error factory receives `IValidationContext`
2. Extracts `rule_status: IValidationRuleStatus` from context
3. Accesses rule definition via `rule_status.rule: IValidationRule`
4. Creates strongly typed error objects with extracted data

**Benefits:**

- Natural data flow through existing context
- No additional extraction interfaces needed
- Type-safe access to all rule information

### Event Transmission Pattern

Rule status provides JSON serialization for event systems:

**Process:**

1. Event system accesses `context.rule_status`
2. Calls `rule_status.to_json()` method
3. Receives complete JSON string with rule and status data
4. Transmits serialized event data

**Benefits:**

- Single method for complete serialization
- Rule status controls its own data representation
- JSON format suitable for external systems

## Validation Requirements

### Type Safety Enforcement

- **FORBIDDEN:** All `Dict[str, Any]` patterns
- **FORBIDDEN:** Metadata dictionaries
- **FORBIDDEN:** Dynamic attribute access (`getattr`, `setattr`, `hasattr`)
- **REQUIRED:** Strongly typed properties and methods only
- **REQUIRED:** Protocol-based interfaces with type annotations

### Single Source of Truth Validation

- Rule definition stored ONLY in `ValidationDescriptor.validation_rule`
- Rule execution state stored ONLY in `ValidationContext.rule_status`
- NO duplication of rule information across layers
- NO string-based rule storage in descriptors

### Immutability Enforcement

- `IValidationRule` objects must be immutable after creation
- `IValidationRule` can be cached and shared across contexts
- `IValidationRuleStatus` is mutable for execution tracking
- Rule reference in status must be immutable

## Testing Strategy

### Unit Tests Required

1. **Interface Compliance:** Verify implementations match protocols
2. **Immutability:** Confirm rule objects cannot be modified
3. **Reference Integrity:** Validate rule status maintains correct rule reference
4. **Serialization:** Test `to_json()` produces valid, complete JSON
5. **Factory Creation:** Verify atomic creation of rule and status objects

### Integration Tests Required

1. **Error Factory:** Confirm error creation from context data
2. **Event Transmission:** Validate event JSON serialization
3. **Context Hierarchy:** Test parent/child context relationships
4. **Factory Workflows:** End-to-end validation context creation

### Migration Tests Required

1. **Property Access:** Verify new property paths work correctly
2. **Backward Compatibility:** Confirm no functionality regression
3. **Type Safety:** Validate no untyped dictionary usage
4. **Performance:** Ensure no significant performance degradation

## Success Criteria

### Architecture Goals Met

- ✅ Single source of truth established
- ✅ Clean separation of immutable definition vs mutable state
- ✅ Type safety enforced throughout system
- ✅ No metadata dictionaries or untyped structures

### Functional Requirements Met

- ✅ Error handling extracts data from context
- ✅ Event transmission uses rule status JSON serialization  
- ✅ Validation contexts maintain rule and status information
- ✅ Factory pattern creates both objects atomically

### Quality Requirements Met

- ✅ All code uses strongly typed objects only
- ✅ No `Dict[str, Any]` or metadata dictionary patterns
- ✅ Full test coverage for new interfaces and implementations
- ✅ Documentation updated to reflect new architecture

## Risk Mitigation

### Breaking Changes

- **Risk:** Existing code accesses old property paths
- **Mitigation:** Comprehensive search and replace, thorough testing

### Performance Impact  

- **Risk:** Additional object creation overhead
- **Mitigation:** Immutable rules can be cached and reused

### Complexity Increase

- **Risk:** More objects to manage
- **Mitigation:** Factory pattern ensures correct object creation

### Type Safety Violations

- **Risk:** Developers revert to untyped patterns
- **Mitigation:** Code review enforcement, linting rules, documentation

## Completion Checklist

### Phase 1 - Interface Creation

- [ ] `IValidationRule` interface defined
- [ ] `IValidationRuleStatus` interface defined  
- [ ] `ValidationRule` implementation created
- [ ] `ValidationRuleStatus` implementation created

### Phase 2 - Descriptor Updates

- [ ] String `validation_rule` removed from all descriptors
- [ ] `IValidationRule` added to all descriptor types
- [ ] `IValidationDescriptor` base interface updated
- [ ] Descriptor constructors require `IValidationRule`

### Phase 3 - Context Updates

- [ ] `IValidationContext` interface updated
- [ ] `ValidationContext` implementation updated
- [ ] Convenience properties implemented
- [ ] Context constructors require `IValidationRuleStatus`

### Phase 4 - Factory Updates

- [ ] `ValidationContextFactory` methods updated
- [ ] Factory creates both rule and status objects
- [ ] Atomic context creation implemented
- [ ] All factory methods support new pattern

### Phase 5 - Usage Pattern Updates

- [ ] Error factory updated for context-based extraction
- [ ] Event system uses `to_json()` method
- [ ] Monitoring accesses rule through status
- [ ] Logging uses structured rule data

### Phase 6 - Migration and Cleanup

- [ ] All property access paths updated
- [ ] Legacy `IActiveRule` interface removed
- [ ] String rule storage eliminated
- [ ] All tests pass with new structure
- [ ] No untyped dictionaries remain in codebase

## Conclusion

This refactoring establishes a clean, type-safe architecture that eliminates information duplication while maintaining clear separation between immutable rule definitions and mutable execution state. The approach addresses current use cases (error handling, event transmission) without over-engineering while providing a solid foundation for future requirements.
