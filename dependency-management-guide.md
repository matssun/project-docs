# Dependency Management Guide

Complete guide for managing dependencies in the modular Python platform.

## Overview

This platform uses a strict dependency hierarchy with standardized pyproject.toml files across all 32+ modules. Dependencies are managed through Poetry with enhanced tooling for automatic lock file management.

## Dependency Hierarchy

The platform follows a strict layered architecture:

### Foundation Layer
- **core_interfaces** - No dependencies (foundation)
- **shared_testing** - Only dev dependencies

### Core Layer  
- **error_handling** - Depends on: core_interfaces
- **validation** - Depends on: core_interfaces, error_handling
- **config_management** - Depends on: core_interfaces, error_handling
- **core_data_structures** - Depends on: core_interfaces

### Infrastructure Layer
- **service_infrastructure** - Depends on: core layer + validation, config_management
- **service_registry** - Depends on: core_interfaces
- **persistence_infrastructure** - Depends on: core layer + service_infrastructure
- **monitoring_infrastructure** - Depends on: core layer + service_infrastructure

### Client/Network Layer
- **core_requests** - Depends on: infrastructure layer
- **client_base** - Depends on: core_requests + infrastructure
- **network_client** - Depends on: client_base + infrastructure
- **network_orchestration** - Depends on: network_client + orchestration

### Domain Layer
- **entsoe_client** - Depends on: client layer + domain-specific deps
- **entsoe_price_service** - Depends on: entsoe_client + service layer

### Security Layer
- **security_core_interfaces** - Depends on: core_interfaces
- **security_*** modules - Depends on: security_core_interfaces + relevant core/infrastructure

## Adding Dependencies

### 1. Local Module Dependencies

Add local platform modules to the `[tool.poetry.dependencies]` section:

```toml
[tool.poetry.dependencies]
python = ">=3.13"

# Local path dependencies
core_interfaces = { path = "../core_interfaces", develop = true }
error_handling = { path = "../error_handling", develop = true }
validation = { path = "../validation", develop = true }
```

**Rules:**
- Always use relative paths (`../module_name`)
- Always include `develop = true`
- Follow the dependency hierarchy (no circular dependencies)
- Never depend on higher-layer modules

### 2. External Dependencies

Add external packages with minimum version constraints:

```toml
[tool.poetry.dependencies]
# HTTP and networking
aiohttp = ">=3.9.1"
httpx = ">=0.25.0"
requests = ">=2.32.0"

# Data handling
pydantic = ">=2.5.0"
lxml = ">=4.9.3"

# Utilities
typing-extensions = ">=4.0.0"
```

**Preferred version format:** `>=X.Y.Z` (minimum version)
**Avoid:** Exact versions (`==`) unless required for compatibility

### 3. Development Dependencies

Add development tools to the dev group:

```toml
[tool.poetry.group.dev.dependencies]
pytest = ">=7.0.0"
pytest-asyncio = ">=0.21.0"
pytest-cov = ">=4.1.0"
pytest-mock = ">=3.10.0"
mypy = "^1.15.0"
black = ">=23.0.0"
isort = ">=5.12.0"
ruff = ">=0.1.0"
shared_testing = {path = "../shared_testing", develop = true}
```

## Managing Lock Files

The enhanced `poetry_setup.sh` script automatically handles lock file management:

### Automatic Lock Detection

The script automatically detects when `poetry lock` is needed:
- When `pyproject.toml` is newer than `poetry.lock`
- When `poetry.lock` fails validation
- When `poetry install` fails due to lock issues

### Manual Lock Management

```bash
# Force lock update
../scripts/poetry_setup.sh --force-lock create

# Skip automatic lock detection  
../scripts/poetry_setup.sh --skip-lock-check create

# Verbose output showing lock analysis
../scripts/poetry_setup.sh --verbose create
```

### Troubleshooting Lock Issues

1. **Dependency conflicts:**
   ```bash
   poetry lock --verbose
   ```

2. **Clear cache and retry:**
   ```bash
   poetry cache clear pypi --all
   poetry lock
   ```

3. **Check for version conflicts:**
   ```bash
   poetry show --tree
   ```

## Common Dependency Patterns

### Core Module Pattern
```toml
[tool.poetry.dependencies]
python = ">=3.13"
# Usually only shared_testing for core modules
shared_testing = { path = "../shared_testing", develop = true }
```

### Infrastructure Module Pattern
```toml
[tool.poetry.dependencies]
python = ">=3.13"
typing-extensions = ">=4.0.0"

# Core dependencies
core_interfaces = { path = "../core_interfaces", develop = true }
error_handling = { path = "../error_handling", develop = true }
config_management = { path = "../config_management", develop = true }

# Infrastructure-specific external deps
redis = ">=5.0.0"
prometheus-client = ">=0.15.0"
```

### Client Module Pattern
```toml
[tool.poetry.dependencies]
python = ">=3.13"

# HTTP dependencies
aiohttp = ">=3.9.1"
httpx = ">=0.25.0"

# Data validation
pydantic = ">=2.5.0"

# Local dependencies (following hierarchy)
core_interfaces = { path = "../core_interfaces", develop = true }
error_handling = { path = "../error_handling", develop = true }
service_infrastructure = { path = "../service_infrastructure", develop = true }
network_client = { path = "../network_client", develop = true }
```

### Domain Module Pattern
```toml
[tool.poetry.dependencies]
python = ">=3.13"

# Domain-specific external dependencies
lxml = ">=4.9.3"
xmlschema = ">=1.0.0"

# Full stack of local dependencies
core_interfaces = { path = "../core_interfaces", develop = true }
error_handling = { path = "../error_handling", develop = true }
validation = { path = "../validation", develop = true }
client_base = { path = "../client_base", develop = true }
entsoe_client = { path = "../entsoe_client", develop = true }
```

## Workflow Examples

### Adding a New Dependency

1. **Edit pyproject.toml:**
   ```toml
   new_package = ">=1.0.0"
   ```

2. **Update environment:**
   ```bash
   ../scripts/poetry_setup.sh recreate
   ```
   The script automatically runs `poetry lock` if needed.

3. **Verify installation:**
   ```bash
   poetry show new_package
   ```

### Adding a Local Module Dependency

1. **Check dependency hierarchy** - Ensure no circular dependencies
2. **Add to pyproject.toml:**
   ```toml
   new_module = { path = "../new_module", develop = true }
   ```
3. **Update environment:**
   ```bash
   ../scripts/poetry_setup.sh --verbose recreate
   ```

### Creating a New Module

1. **Use setup command:**
   ```bash
   /setup-module my_new_module
   ```
   This creates the module with minimal dependencies.

2. **Add dependencies as needed:**
   Edit the generated `pyproject.toml` following the patterns above.

3. **Update environment:**
   The setup command automatically creates the poetry environment.

## Best Practices

### Version Management
- **Use minimum versions** (`>=X.Y.Z`) for flexibility
- **Pin critical versions** only when necessary for compatibility
- **Update regularly** but test thoroughly
- **Document breaking changes** in module CLAUDE.md files

### Dependency Organization
- **Group by purpose** - HTTP, data processing, testing, etc.
- **Comment complex dependencies** - Explain why specific versions are needed
- **Keep dev dependencies current** - Especially linting and testing tools
- **Minimize external dependencies** - Prefer platform modules when possible

### Testing Dependencies
- **Always add shared_testing** to dev dependencies
- **Include testing utilities** - pytest-mock, pytest-cov, etc.
- **Test with minimal deps** - Ensure module works with minimum versions
- **Test dependency updates** - Verify compatibility before committing

### Documentation
- **Update dependencies.md** in each module's `.claude/` folder
- **Document breaking changes** when updating major versions
- **Explain complex dependencies** - Why they're needed, alternatives considered
- **Keep README.md current** with installation instructions

## Troubleshooting

### Common Issues

1. **Circular dependency error:**
   - Check dependency hierarchy
   - Move common code to lower-layer module
   - Use dependency injection patterns

2. **Poetry lock fails:**
   - Check for version conflicts: `poetry show --tree`
   - Clear cache: `poetry cache clear pypi --all`
   - Update conflicting packages

3. **Module not found:**
   - Ensure develop=true for local dependencies
   - Check path is correct (`../module_name`)
   - Verify target module exists

4. **Version conflicts:**
   - Use `poetry show --why package_name`
   - Consider relaxing version constraints
   - Update conflicting dependencies

### Getting Help

1. **Check module's CLAUDE.md** - Module-specific dependency info
2. **Review this guide** - Common patterns and solutions
3. **Use verbose mode** - `--verbose` flag shows detailed analysis
4. **Check poetry documentation** - For advanced dependency management

## Migration Notes

### From Old Format
The standardization updated all modules to:
- Python 3.13 target
- Consistent build system (setuptools)
- Standardized tool configurations
- Proper dependency declarations

### Breaking Changes
- All modules now require Python 3.13+
- Standardized mypy/black/ruff configurations
- Consistent project metadata format

No action needed - all modules have been updated automatically.