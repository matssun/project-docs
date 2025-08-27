# Coding Standards and Rules

This directory contains the mandatory coding standards for all code in this project. These rules are **non-negotiable** and must be followed by all developers.

## Core Principles

### 1. Fail Fast Philosophy
All code must fail immediately when dependencies are not available or when invalid conditions are detected. No silent failures or degraded functionality.

### 2. Explicit Dependencies
All dependencies must be declared explicitly in `pyproject.toml` files. No optional or conditional dependencies in production code.

### 3. Clean Architecture
Follow the established architectural patterns and dependency hierarchies. No circular dependencies or architectural violations.

## Mandatory Rules

### 🚫 Import Rules - **CRITICAL**
**File**: [import-rules.md](./import-rules.md)

**Summary**: NO conditional imports, NO try/except around imports, NO optional dependencies in production code.

**Key Requirements**:
- All imports must be direct and fail immediately if dependencies are not available
- No `try/except ImportError` patterns
- No mock classes in production code
- All dependencies must be declared in `pyproject.toml`

**Enforcement**: Any PR with conditional imports will be **automatically rejected**.

### 📝 Future Rules
Additional coding standards will be added here as needed:
- Code formatting standards
- Documentation requirements  
- Error handling patterns
- Testing requirements

## Enforcement

### Automated Checks
- Import pattern linting in CI/CD pipeline
- Dependency declaration validation
- Architecture compliance checks

### Code Review Requirements
- All PRs must pass coding standards review
- Reviewers must verify compliance with all rules
- No exceptions without architectural team approval

## Rationale

These rules ensure:
1. **Predictable Behavior** - Code works the same way in all environments
2. **Immediate Feedback** - Problems are caught at startup, not runtime
3. **Clear Dependencies** - All requirements are explicit and visible
4. **Maintainable Code** - No hidden dependencies or surprising behaviors
5. **Production Safety** - No runtime surprises due to missing dependencies

## Violation Reporting

If you find code that violates these standards:
1. Create an issue with the `coding-standards-violation` label
2. Include the file path and specific violation
3. Suggest the correct implementation approach
4. Tag the module owner for immediate attention

**Remember**: These are not suggestions - they are mandatory requirements for code quality and system reliability.