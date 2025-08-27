# Metadata Removal Project Plan

## Overview

**Objective**: Remove all untyped metadata structures and replace them with structured object-oriented classes from core_interfaces across all submodules.

**Status**: Core interfaces complete - serves as design template for all other modules.

**Approach**: Systematic module-by-module conversion using core_interfaces patterns as the gold standard.

---

## Phase 1: Assessment and Foundation (1-2 sprints)

### Sprint 1.1: Code Analysis

- **Task**: Audit all submodules for metadata usage patterns
- **Focus Areas**:
  - Search for `hasattr()`/`getattr()` usage patterns
  - Find `metadata` dictionary usage
  - Identify `Any` ty   pe declarations
  - Locate untyped dictionary structures
- **Deliverable**: Complete inventory of conversion targets per module

### Sprint 1.2: Pattern Documentation  

- **Task**: Document core_interfaces design patterns
- **Focus Areas**:
  - Extract reusable patterns from completed core_interfaces
  - Document typed object creation patterns
  - Document protocol-based access patterns
  - Create conversion guidelines template
- **Deliverable**: Design pattern guide for conversion teams

---

## Phase 2: High-Impact Module Conversion (3-4 sprints)

### Sprint 2.1: Validation Module

**Priority**: High (foundation module)

**Current Issues**:

- `add_metadata()` calls in validation state
- hasattr/getattr patterns in active_rule.py  
- Metadata dictionaries in xml_schema_wrapper.py
- Untyped context information handling

**Target State**:

- Replace `add_metadata()` with typed descriptor properties
- Convert dynamic attribute access to protocol-based access
- Use typed validation_details instead of metadata dicts
- Implement structured validation context objects

**Estimated Effort**: 8-12 story points

### Sprint 2.2: Error Handling Module  

**Priority**: High (cross-cutting concern)

**Current Issues**:

- hasattr/getattr patterns in validation_error_strategies.py
- Metadata extraction from context objects
- Dynamic attribute access for error details

**Target State**:

- Protocol-based error context access
- Typed error detail structures
- Structured error information objects

**Estimated Effort**: 6-8 story points

### Sprint 2.3: Service Infrastructure Module

**Priority**: Medium (infrastructure foundation)

**Current Issues**:

- Untyped configuration dictionaries
- Metadata structures in monitoring
- Dynamic configuration access patterns

**Target State**:

- Protocol-based settings classes
- ValidationToErrorContextBridge integration
- Typed configuration objects

**Estimated Effort**: 6-10 story points

---

## Phase 3: Supporting Module Conversion (2-3 sprints)

### Sprint 3.1: Core Requests Module

**Priority**: Medium

**Current Issues**:

- Any types in parameter handling
- Untyped metadata dictionaries  
- Dynamic response parsing

**Target State**:

- TypedDict structures for metadata
- Specific Union types replacing Any
- Typed response objects

**Estimated Effort**: 4-6 story points

### Sprint 3.2: Additional Submodules

**Priority**: Low-Medium

**Scope**: Handle remaining modules based on discovery from Phase 1

- Convert remaining metadata usage
- Apply core_interfaces patterns consistently
- Ensure protocol-based access throughout

**Estimated Effort**: 6-12 story points (variable based on findings)

---

## Phase 4: Integration and Validation (1-2 sprints)

### Sprint 4.1: System Integration

- **Task**: End-to-end testing of converted modules
- **Focus**: Verify no metadata dictionaries remain
- **Testing**: Run comprehensive type checking
- **Documentation**: Update architectural documentation

### Sprint 4.2: Cleanup and Optimization

- **Task**: Final cleanup and performance optimization
- **Focus**: Remove deprecated metadata handling code
- **Validation**: Confirm all hasattr/getattr usage eliminated
- **Deliverable**: Clean, fully typed codebase

---

## Success Criteria

### Technical Goals

- ✅ Zero usage of `hasattr()`/`getattr()` for business logic
- ✅ Zero untyped metadata dictionaries  
- ✅ Zero `Any` types except where absolutely necessary
- ✅ All validation contexts use structured objects
- ✅ All error handling uses protocol-based access
- ✅ Complete type safety across all modules

### Quality Gates  

- All existing tests pass
- Type checking passes without warnings
- No dynamic attribute access patterns
- Full compliance with core_interfaces patterns

---

## Risk Mitigation

**Risk**: Breaking existing functionality during conversion
**Mitigation**:

- Convert one module at a time
- Maintain backward compatibility during transition
- Comprehensive test coverage for each conversion

**Risk**: Performance impact from increased type checking
**Mitigation**:

- Benchmark before/after conversion
- Optimize hot paths if needed
- Use runtime type checking judiciously

**Risk**: Team learning curve for new patterns
**Mitigation**:

- Provide pattern documentation from Phase 1
- Code review focus on pattern compliance
- Regular knowledge sharing sessions

---

## Implementation Notes for Claude Code

### Key Patterns to Follow (from core_interfaces)

1. **Typed Descriptors**: Use structured classes like `ValidationDescriptor` instead of metadata dicts
2. **Protocol Access**: Replace `hasattr(obj, 'attr')` with `isinstance(obj, Protocol)`
3. **Structured State**: Use `IValidationState` interface instead of dynamic state modification
4. **Factory Patterns**: Use typed factories for object creation with explicit parameters

### Code Quality Rules

- Never use `Any` types without explicit justification
- No `metadata` dictionaries - use typed structures
- No `hasattr`/`getattr` for business logic access
- All objects must implement appropriate protocols
- Full docstring coverage for all new/modified code

### Testing Requirements

- Unit tests for all converted components
- Integration tests for cross-module interactions  
- Type checking validation in CI/CD pipeline
- Performance regression testing

---

**Total Estimated Timeline**: 8-11 sprints (16-22 weeks)
**Resource Requirements**: 2-3 developers familiar with the codebase
**Success Metrics**: 100% metadata elimination, full type safety, zero dynamic attribute access
