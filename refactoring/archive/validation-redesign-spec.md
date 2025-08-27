# Validation Architecture Redesign Specification

## Executive Summary

This document specifies the redesign of the validation system to implement a clean separation between rule definitions, constraint management, and business logic execution. The new architecture introduces `ValidationProcess` as the central container for ordered rule execution while maintaining strict OOP principles.

## Core Conceptual Model

### ValidationRule Container

```
ValidationRule = BusinessRule + List[Constraints] + ConstraintLogic
```

- **Static container** with no evaluation state
- **BusinessRule**: Core business logic implementation
- **Constraints**: List of atomic validation constraints
- **ConstraintLogic**: Orchestration logic for combining constraint results

### ValidationProcess Container

```
ValidationProcess = {
  ordered_rules: List[Tuple[IValidationRule, IValidationRuleStatus, List[IValidationIssue]]]
  outcome: IValidationOutcome
  orchestrator: IValidationOrchestrator
  rule_builder: IValidationRuleBuilder  
  rule_evaluator: IValidationRuleEvaluator
}
```

## Key Design Principles

1. **Rule order matters** → ordered list execution
2. **No untyped dictionaries** → strongly typed objects only
3. **Clear ownership boundaries** → ValidationState owns ValidationProcess
4. **Separation of concerns** → building ≠ orchestration ≠ evaluation
5. **Factory pattern usage** → for constraint evaluators and business rules

## New Interfaces Required

### Core Process Interface

```python
@runtime_checkable
class IValidationProcess(Protocol):
    ordered_rules: List[Tuple[IValidationRule, IValidationRuleStatus, List[IValidationIssue]]]
    outcome: IValidationOutcome
    orchestrator: IValidationOrchestrator
    rule_builder: IValidationRuleBuilder
    rule_evaluator: IValidationRuleEvaluator
    
    def add_rule(self, rule: IValidationRule) -> None: ...
    def remove_rule(self, rule_id: IRuleID) -> bool: ...
    def evaluate_all_rules(self, context: IValidationContext) -> None: ...
    def get_rule_status(self, rule_id: IRuleID) -> Optional[IValidationRuleStatus]: ...
```

### Business Rule Interface

```python
@runtime_checkable
class IBusinessRule(Protocol):
    rule_id: IRuleID
    rule_name: str
    
    def evaluate(self, constraint_results: List[ConstraintEvaluationResult], context: IValidationContext) -> BusinessRuleResult: ...
    def get_required_constraints(self) -> List[IValidationConstraint]: ...
```

### Orchestration Interface

```python
@runtime_checkable
class IValidationOrchestrator(Protocol):
    def execute_rules_in_order(self, rules: List[Tuple[IValidationRule, IValidationRuleStatus, List[IValidationIssue]]], context: IValidationContext) -> IValidationOutcome: ...
    def handle_rule_dependencies(self, rules: List[IValidationRule]) -> List[IValidationRule]: ...
```

### Rule Builder Interface

```python
@runtime_checkable
class IValidationRuleBuilder(Protocol):
    def build_rule(self, business_rule: IBusinessRule, constraints: List[IValidationConstraint]) -> IValidationRule: ...
    def add_constraint(self, constraint: IValidationConstraint) -> IValidationRuleBuilder: ...
    def set_business_rule(self, business_rule: IBusinessRule) -> IValidationRuleBuilder: ...
```

### Rule Evaluator Interface

```python
@runtime_checkable
class IValidationRuleEvaluator(Protocol):
    def evaluate_rule(self, rule: IValidationRule, context: IValidationContext, constraint_evaluator: IConstraintEvaluator) -> RuleEvaluationResult: ...
    def update_rule_status(self, rule_status: IValidationRuleStatus, result: RuleEvaluationResult) -> None: ...
```

## Modified Interfaces

### IValidationRule Enhancement

```python
# ADD to existing interface:
business_rule: IBusinessRule
constraints: List[IValidationConstraint]
constraint_logic: IConstraintLogic

def get_business_rule(self) -> IBusinessRule: ...
def get_constraints(self) -> List[IValidationConstraint]: ...
```

### IValidationState Enhancement

```python
# ADD to existing interface:
validation_process: Optional[IValidationProcess]

def set_validation_process(self, process: IValidationProcess) -> None: ...
def get_validation_process(self) -> Optional[IValidationProcess]: ...
```

## Descriptor Cleanup

### Problem Resolution

**Current Issue**: `IValidationDescriptor.validation_rule` property creates confusion with actual `IValidationRule` objects.

**Solution**: Replace with rule reference by ID:

```python
# MODIFY IValidationDescriptor:
# REMOVE: validation_rule: str
# ADD: rule_reference_id: Optional[IRuleID]
```

## Implementation Files

### New Files to Create

1. **Core Process**
   - `core_interfaces/src/core_interfaces/interfaces/validation/process/ivalidation_process.py`
   - `validation/src/validation/process/validation_process.py`

2. **Business Rule System**
   - `core_interfaces/src/core_interfaces/interfaces/validation/business/ibusiness_rule.py`
   - `validation/src/validation/business/business_rule.py`
   - `validation/src/validation/business/business_rule_factory.py`

3. **Orchestration**
   - `core_interfaces/src/core_interfaces/interfaces/validation/orchestration/ivalidation_orchestrator.py`
   - `validation/src/validation/orchestration/validation_orchestrator.py`

4. **Rule Building**
   - `core_interfaces/src/core_interfaces/interfaces/validation/building/ivalidation_rule_builder.py`
   - `validation/src/validation/building/validation_rule_builder.py`

5. **Rule Evaluation**
   - `core_interfaces/src/core_interfaces/interfaces/validation/evaluation/ivalidation_rule_evaluator.py`
   - `validation/src/validation/evaluation/validation_rule_evaluator.py`

### Files to Modify

1. **Interface Updates**
   - `core_interfaces/src/core_interfaces/interfaces/validation/rules/ivalidation_rule.py`
   - `core_interfaces/src/core_interfaces/interfaces/state/ivalidation_state.py`
   - `core_interfaces/src/core_interfaces/interfaces/validation/constraints/ivalidation_descriptor.py`

2. **Implementation Updates**
   - `validation/src/validation/rules/validation_rule.py`
   - `validation/src/validation/state/validation_state.py`
   - `validation/src/validation/state/validation_descriptor.py`

3. **Context Integration**
   - `validation/src/validation/context/validation_context.py`

### Files to Delete

1. **Redundant Rule Management**
   - `validation/src/validation/validation_process/active_rule.py` (replaced by ValidationProcess)

## Development Phases

### Phase 1: Core Interfaces

- Create all new interface files
- Modify existing interfaces
- Update package exports

### Phase 2: Business Rule System  

- Implement IBusinessRule and factory
- Create concrete business rule implementations
- Integrate with constraint system

### Phase 3: Process Container

- Implement ValidationProcess
- Create orchestrator, builder, evaluator
- Integrate with existing constraint evaluation

### Phase 4: Integration & Cleanup

- Update ValidationState and ValidationContext
- Modify descriptors to remove validation_rule property
- Delete obsolete files
- Update all imports and dependencies

### Phase 5: Testing & Validation

- Update all tests for new architecture
- Verify constraint evaluation integration
- Test multi-rule scenarios

## Integration Points

### With Existing Constraint System

- ValidationRuleEvaluator uses existing `IConstraintEvaluationCoordinator`
- BusinessRule implementations get constraints via `IConstraintEvaluatorFactory`
- No changes to constraint evaluation logic

### With ValidationCoordinator

- ValidationCoordinator delegates rule evaluation to ValidationProcess
- Maintains existing constraint management responsibilities
- Uses ValidationProcess for multi-rule scenarios

## Validation Requirements

1. **Type Safety**: All components must use strongly typed interfaces
2. **Immutability**: ValidationRule remains immutable after creation
3. **Factory Pattern**: All evaluators created via factories
4. **Clean Separation**: Building ≠ Orchestration ≠ Evaluation
5. **Backward Compatibility**: Existing constraint evaluation unchanged

## Success Criteria

- [ ] Single rule validation works as before
- [ ] Multi-rule validation works with proper ordering
- [ ] Constraint evaluation integrates seamlessly
- [ ] No untyped dictionaries or metadata structures
- [ ] Clear ownership boundaries maintained
- [ ] All existing tests pass after refactoring
