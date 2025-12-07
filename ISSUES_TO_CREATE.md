# GitHub Issues to Create - Priority List

This document provides ready-to-use GitHub issue templates based on the PROJECT_REVIEW.md findings.

**Total Issues to Create:** 16  
**Review Date:** December 7, 2024

---

## Critical Priority Issues (P0)

### Issue 1: Fix Invalid Dependencies in requirements.txt

**Title:** Fix requirements.txt - Remove stdlib modules and add version constraints

**Labels:** `bug`, `dependencies`, `P0-critical`, `good first issue`

**Description:**
```markdown
## Problem
The `requirements.txt` file contains Python standard library modules that should not be listed as dependencies:
- `uuid` (line 3)
- `logging` (line 4)

Additionally, dependencies lack version constraints which can lead to breaking changes and inconsistent behavior across environments.

## Current State
```txt
pandas
pyyaml
uuid
logging
```

## Expected State
```txt
pandas>=2.0.0,<3.0.0
pyyaml>=6.0,<7.0
```

## Impact
- Confusing for new contributors
- May cause installation issues with some package managers
- Unpredictable behavior across different installations
- Potential security vulnerabilities from outdated packages

## Tasks
- [ ] Remove `uuid` from requirements.txt
- [ ] Remove `logging` from requirements.txt
- [ ] Add version constraint to `pandas` (>=2.0.0,<3.0.0)
- [ ] Add version constraint to `pyyaml` (>=6.0,<7.0)
- [ ] Test installation with updated requirements

## References
- See PROJECT_REVIEW.md Issue #1 and #2
- Related PRODUCT_ROADMAP.md TASK-011
```

**Assignee:** Any contributor  
**Milestone:** v0.2.0

---

### Issue 2: Add SQL Query Validation for Security

**Title:** Implement SQL query safety validation to prevent injection vulnerabilities

**Labels:** `security`, `enhancement`, `P0-critical`

**Description:**
```markdown
## Problem
In `infra/AnswerValidator.py`, SQL queries are executed without safety validation. While queries are currently loaded from trusted files, there's no protection if user input is ever accepted in the future.

## Location
File: `infra/AnswerValidator.py`, line 85

```python
def execute_query(self) -> None:
    # ...
    self.answer_df = pd.read_sql_query(self.query, conn, index_col=None)
```

## Security Concern
- Potential SQL injection if user input is ever accepted
- No validation that queries don't contain malicious patterns
- Future feature additions could introduce vulnerabilities

## Proposed Solution

Add query validation before execution:

```python
def _validate_query_safety(self, query: str) -> bool:
    """
    Validate that query doesn't contain dangerous patterns.
    
    Args:
        query: SQL query string to validate
        
    Returns:
        True if query is safe
        
    Raises:
        SecurityError: If query contains forbidden operations
    """
    # Only allow SELECT queries for practice platform
    forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 
                         'ALTER', 'CREATE', 'TRUNCATE', 'EXEC']
    
    query_upper = query.strip().upper()
    
    # Ensure query starts with SELECT or WITH (for CTEs)
    if not (query_upper.startswith('SELECT') or query_upper.startswith('WITH')):
        raise SecurityError("Only SELECT queries are allowed")
    
    # Check for forbidden keywords
    for keyword in forbidden_keywords:
        if keyword in query_upper:
            raise SecurityError(f"Query contains forbidden operation: {keyword}")
    
    return True
```

## Tasks
- [ ] Create SecurityError exception class
- [ ] Implement `_validate_query_safety()` method
- [ ] Call validation in `execute_query()` before execution
- [ ] Add unit tests for query validation
- [ ] Add tests for malicious query detection
- [ ] Document security assumptions in code comments
- [ ] Update README with security documentation

## Impact
- Prevents potential SQL injection attacks
- Makes future feature development safer
- Establishes security best practices

## References
- PROJECT_REVIEW.md Issue #8
- OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
```

**Assignee:** Security-focused contributor  
**Milestone:** v0.2.0

---

## High Priority Issues (P1)

### Issue 3: Create requirements-dev.txt for Development Dependencies

**Title:** Add requirements-dev.txt for development dependencies

**Labels:** `enhancement`, `dependencies`, `P1-high`, `good first issue`

**Description:**
```markdown
## Problem
No `requirements-dev.txt` file exists for development dependencies. Developers need to manually discover and install testing/linting tools.

## Impact
- Developers need to manually install testing/linting tools
- No standardized development environment
- CI/CD pipeline requirements not documented
- Inconsistent tooling across contributors

## Proposed Solution

Create `requirements-dev.txt`:

```txt
# Testing
pytest>=7.4.0,<8.0.0
pytest-cov>=4.1.0,<5.0.0

# Code Quality
flake8>=6.0.0,<7.0.0
black>=23.0.0,<24.0.0
isort>=5.12.0,<6.0.0
pylint>=2.17.0,<3.0.0

# Type Checking
mypy>=1.4.0,<2.0.0

# Documentation
sphinx>=7.0.0,<8.0.0

# Security
bandit>=1.7.0,<2.0.0
safety>=2.3.0,<3.0.0
```

## Tasks
- [ ] Create `requirements-dev.txt` file
- [ ] Add testing dependencies (pytest, pytest-cov)
- [ ] Add linting dependencies (flake8, black, isort, pylint)
- [ ] Add type checking dependencies (mypy)
- [ ] Add documentation dependencies (sphinx)
- [ ] Add security scanning dependencies (bandit, safety)
- [ ] Update README.md with development setup instructions
- [ ] Update CONTRIBUTING.md (if exists) with tooling information

## Installation Command
After creation, developers can install with:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## References
- PROJECT_REVIEW.md Issue #3
```

**Assignee:** Any contributor  
**Milestone:** v0.2.0

---

### Issue 4: Implement CI/CD Pipeline with GitHub Actions

**Title:** Add GitHub Actions workflow for CI/CD

**Labels:** `infrastructure`, `ci/cd`, `P1-high`

**Description:**
```markdown
## Problem
No automated CI/CD pipeline exists. Code quality issues may be merged without detection.

## Missing Automation
- Running tests on PR
- Linting code
- Type checking
- Security scanning
- Coverage reporting

## Impact
- Code quality issues may be merged
- No automated testing before merge
- Manual review burden on maintainers
- Inconsistent code quality

## Proposed Solution

Create `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    name: Lint Code
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install flake8 black isort mypy
      
      - name: Run flake8
        run: flake8 infra/ tests/ --max-line-length=100
      
      - name: Check code formatting with black
        run: black --check infra/ tests/
      
      - name: Check import sorting
        run: isort --check-only infra/ tests/
      
      - name: Run mypy type checking
        run: mypy infra/ --ignore-missing-imports

  test:
    name: Run Tests
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests with coverage
        run: |
          pytest tests/ -v --cov=infra --cov-report=xml --cov-report=term
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install bandit safety
      
      - name: Run bandit security scan
        run: bandit -r infra/ -ll
      
      - name: Check dependencies for vulnerabilities
        run: safety check --json
```

## Tasks
- [ ] Create `.github/workflows/ci.yml`
- [ ] Add lint job (flake8, black, isort, mypy)
- [ ] Add test job with matrix for Python 3.10, 3.11, 3.12
- [ ] Add security scan job (bandit, safety)
- [ ] Configure codecov for coverage reporting
- [ ] Add status badges to README.md
- [ ] Test workflow with a PR
- [ ] Document CI/CD process in CONTRIBUTING.md

## References
- PROJECT_REVIEW.md Issue #13
- PRODUCT_ROADMAP.md TASK-014
```

**Assignee:** DevOps-focused contributor  
**Milestone:** v0.2.0

---

### Issue 5: Increase Test Coverage for Core Modules

**Title:** Add comprehensive tests for AnswerValidator and logging_config

**Labels:** `testing`, `P1-high`, `enhancement`

**Description:**
```markdown
## Problem
Critical modules lack test coverage:
- `infra/AnswerValidator.py` - No tests found
- `infra/logging_config.py` - No tests found
- Integration tests missing for `SQl_answer.py`

## Current Coverage
Existing tests:
- ✅ `test_data_generator.py` - Basic tests
- ✅ `test_difficulty.py` - Difficulty system tests
- ✅ `test_user_system.py` - User management tests

Missing:
- ❌ AnswerValidator tests
- ❌ Logging configuration tests
- ❌ Integration tests
- ❌ Edge case tests

## Impact
- Unknown bugs may exist
- Refactoring is risky
- No confidence in code changes
- Hard to maintain code quality

## Proposed Solution

### Create `tests/test_answer_validator.py`

```python
import pytest
import pandas as pd
from pathlib import Path
from infra.AnswerValidator import AnswerValidator

class TestAnswerValidator:
    @pytest.fixture
    def sample_db(self, tmp_path):
        """Create a sample database for testing."""
        # Setup code
        pass
    
    @pytest.fixture
    def validator(self, tmp_path):
        """Create test validator instance."""
        return AnswerValidator(
            base_dir=tmp_path,
            question_name='test_question'
        )
    
    def test_initialization_with_question_name(self, tmp_path):
        """Test validator initialization with question name."""
        validator = AnswerValidator(
            base_dir=tmp_path,
            question_name='sql_basic_select'
        )
        assert validator.base_dir == tmp_path
        assert validator.question_path.name == 'sql_basic_select'
    
    def test_initialization_with_answer_path(self, tmp_path):
        """Test validator initialization with direct answer path."""
        answer_path = tmp_path / 'solution.sql'
        answer_path.write_text('SELECT * FROM test;')
        
        validator = AnswerValidator(answer_path=answer_path)
        assert validator.db_filename == answer_path
    
    def test_load_sql_valid_file(self, validator, tmp_path):
        """Test loading valid SQL file."""
        # Test implementation
        pass
    
    def test_load_sql_missing_file(self, validator):
        """Test handling of missing SQL file."""
        with pytest.raises(FileNotFoundError):
            validator.load_sql()
    
    def test_execute_query_success(self, validator, sample_db):
        """Test successful query execution."""
        # Test implementation
        pass
    
    def test_execute_query_invalid_sql(self, validator):
        """Test handling of invalid SQL."""
        validator.query = "INVALID SQL SYNTAX"
        with pytest.raises(Exception):
            validator.execute_query()
    
    def test_validate_answer_correct(self, validator):
        """Test validation of correct answer."""
        # Test implementation
        pass
    
    def test_validate_answer_incorrect(self, validator):
        """Test validation of incorrect answer."""
        # Test implementation
        pass
    
    def test_validate_dataframe_structure_mismatch(self, validator):
        """Test DataFrame structure validation with mismatched columns."""
        df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        df2 = pd.DataFrame({'a': [1, 2], 'c': [3, 4]})
        
        with pytest.raises(ValueError):
            validator._validate_dataframe_structure(df1, df2)
    
    def test_compare_dataframes_identical(self, validator):
        """Test comparison of identical DataFrames."""
        df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        df2 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        
        assert validator._compare_dataframes(df1, df2) is True
    
    def test_compare_dataframes_different(self, validator):
        """Test comparison of different DataFrames."""
        df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        df2 = pd.DataFrame({'a': [1, 3], 'b': [3, 4]})
        
        assert validator._compare_dataframes(df1, df2) is False
```

### Create `tests/test_logging_config.py`

```python
import pytest
import logging
from pathlib import Path
from infra.logging_config import LoggerManager

class TestLoggingConfig:
    def test_logger_creation(self, tmp_path):
        """Test logger creation with custom question name."""
        # Test implementation
        pass
    
    def test_log_file_creation(self, tmp_path):
        """Test that log file is created."""
        # Test implementation
        pass
    
    def test_multiple_loggers(self, tmp_path):
        """Test creating multiple loggers doesn't create duplicates."""
        # Test implementation
        pass
```

## Tasks
- [ ] Create `tests/test_answer_validator.py`
- [ ] Create `tests/test_logging_config.py`
- [ ] Create `tests/test_integration.py` for end-to-end tests
- [ ] Add fixtures for test data and databases
- [ ] Aim for 80%+ code coverage
- [ ] Run coverage report: `pytest --cov=infra --cov-report=html`
- [ ] Document testing approach in README

## Coverage Goal
Target: 80%+ coverage for all modules in `infra/`

## References
- PROJECT_REVIEW.md Issue #12
- PRODUCT_ROADMAP.md TASK-010
```

**Assignee:** Testing-focused contributor  
**Milestone:** v0.3.0

---

## Medium Priority Issues (P2)

### Issue 6: Add Comprehensive Type Hints to Codebase

**Title:** Add complete type hints to all public methods and functions

**Labels:** `code-quality`, `P2-medium`, `enhancement`

**Description:**
```markdown
## Problem
While some files have type hints (e.g., `user.py`, `DataGenerator.py`), many functions lack complete type annotations.

## Examples of Missing Type Hints

In `infra/logging_config.py`:
```python
# Current - No type hints
def create_logger(self, logger_name):
    ...

# Should be:
def create_logger(self, logger_name: str) -> logging.Logger:
    ...
```

## Impact
- Reduced code readability
- Harder to catch type-related bugs
- Poor IDE autocomplete support
- Not following modern Python best practices (PEP 484)

## Tasks
- [ ] Add type hints to `infra/logging_config.py`
- [ ] Add type hints to `SQl_answer.py`
- [ ] Review and complete type hints in `infra/AnswerValidator.py`
- [ ] Review and complete type hints in `infra/DataGenerator.py`
- [ ] Add type hints to all test files
- [ ] Run mypy to validate type hints: `mypy infra/ --strict`
- [ ] Update any dynamically typed sections with proper annotations
- [ ] Document type hint conventions in CONTRIBUTING.md

## Type Hint Guidelines
- Use `typing.Optional[T]` for nullable types
- Use `typing.Union[T1, T2]` for multiple allowed types
- Use `typing.List[T]`, `typing.Dict[K, V]` for collections
- Use `typing.Any` sparingly, only when truly necessary
- Add return type annotations to all functions
- Use `-> None` for functions without return value

## References
- PROJECT_REVIEW.md Issue #4
- PEP 484: https://www.python.org/dev/peps/pep-0484/
- PEP 526: https://www.python.org/dev/peps/pep-0526/
```

**Assignee:** Any contributor  
**Milestone:** v0.3.0

---

### Issue 7: Implement Consistent Error Handling Pattern

**Title:** Add comprehensive error handling across all modules

**Labels:** `code-quality`, `P2-medium`, `enhancement`

**Description:**
```markdown
## Problem
Error handling is inconsistent across modules. Some methods have try-except blocks while others let exceptions propagate without context.

## Examples

In `DataGenerator.py`:
```python
# Current - No error handling
def load_yaml_config(self, yaml_file: Union[Path, str]) -> None:
    with open(yaml_file, 'r') as file:
        self.config = yaml.safe_load(file)
```

## Impact
- Unclear error messages for users
- Potential for unhandled exceptions
- Difficult debugging
- Poor user experience

## Proposed Solution

Implement consistent error handling:

```python
def load_yaml_config(self, yaml_file: Union[Path, str]) -> None:
    """
    Load YAML configuration from file.
    
    Args:
        yaml_file: Path to YAML configuration file
        
    Raises:
        FileNotFoundError: If configuration file doesn't exist
        ValueError: If YAML configuration is invalid
    """
    try:
        yaml_path = Path(yaml_file)
        if not yaml_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {yaml_path}\n"
                f"Please ensure the file exists at the specified location."
            )
        
        with open(yaml_path, 'r') as file:
            self.config = yaml.safe_load(file)
            
        if not isinstance(self.config, dict):
            raise ValueError(
                f"Invalid YAML configuration: expected dict, got {type(self.config)}"
            )
            
    except yaml.YAMLError as e:
        raise ValueError(
            f"Invalid YAML syntax in {yaml_path}:\n{str(e)}"
        )
```

## Tasks
- [ ] Add error handling to `DataGenerator.load_yaml_config()`
- [ ] Add error handling to `DataGenerator.write_to_csv()`
- [ ] Add error handling to `DataGenerator.save_to_sqlite()`
- [ ] Add error handling to file I/O operations in `AnswerValidator`
- [ ] Add error handling to `LoggerManager` initialization
- [ ] Create custom exception classes if needed
- [ ] Add error handling documentation
- [ ] Add tests for error conditions

## Error Handling Guidelines
1. Catch specific exceptions, not broad `Exception`
2. Provide context in error messages
3. Include suggestions for resolution
4. Log errors before re-raising
5. Document all raised exceptions in docstrings

## References
- PROJECT_REVIEW.md Issue #5
```

**Assignee:** Any contributor  
**Milestone:** v0.3.0

---

### Issue 8: Create pyproject.toml for Modern Python Packaging

**Title:** Add pyproject.toml for PEP 517/518 compliance

**Labels:** `infrastructure`, `P2-medium`, `enhancement`

**Description:**
```markdown
## Problem
The project lacks a proper package configuration file, preventing:
- Installation as editable package (`pip install -e .`)
- Proper dependency management
- Following modern Python packaging standards

## Impact
- Cannot install project as package
- Import path issues
- Not following PEP 517/518 standards
- Harder to distribute

## Proposed Solution

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "practic-questions-platform"
version = "0.1.0"
description = "SQL Practice Questions Platform with AI assistance"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "SQL Practice Platform Team"}
]
keywords = ["sql", "education", "practice", "learning"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Topic :: Education",
    "Topic :: Database",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "pandas>=2.0.0,<3.0.0",
    "pyyaml>=6.0,<7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0,<8.0.0",
    "pytest-cov>=4.1.0,<5.0.0",
    "flake8>=6.0.0,<7.0.0",
    "black>=23.0.0,<24.0.0",
    "mypy>=1.4.0,<2.0.0",
]

[project.urls]
Homepage = "https://github.com/moshesham/Practic_Questions_Platform"
Documentation = "https://github.com/moshesham/Practic_Questions_Platform/blob/main/README.md"
Repository = "https://github.com/moshesham/Practic_Questions_Platform"
"Bug Tracker" = "https://github.com/moshesham/Practic_Questions_Platform/issues"

[tool.setuptools]
package-dir = {"" = "."}
packages = ["infra"]

[tool.setuptools.package-data]
infra = ["config/*.yml"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=infra --cov-report=term --cov-report=html"

[tool.black]
line-length = 100
target-version = ['py310', 'py311', 'py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
follow_imports = "normal"

[[tool.mypy.overrides]]
module = [
    "pandas.*",
    "yaml.*",
]
ignore_missing_imports = true

[tool.coverage.run]
source = ["infra"]
omit = ["tests/*", "*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

## Tasks
- [ ] Create `pyproject.toml` with above configuration
- [ ] Test installation: `pip install -e .`
- [ ] Test dev installation: `pip install -e ".[dev]"`
- [ ] Update README.md installation instructions
- [ ] Update Dockerfile to use pyproject.toml
- [ ] Verify all tools (black, mypy, pytest) use config from pyproject.toml
- [ ] Remove redundant configuration files if any

## After Creation
Developers can install with:
```bash
# Regular installation
pip install -e .

# Development installation with all tools
pip install -e ".[dev]"
```

## References
- PROJECT_REVIEW.md Issue #15
- PRODUCT_ROADMAP.md TASK-001
- PEP 517: https://peps.python.org/pep-0517/
- PEP 518: https://peps.python.org/pep-0518/
```

**Assignee:** Any contributor  
**Milestone:** v0.3.0

---

### Issue 9: Add Input Validation to DataGenerator

**Title:** Implement input validation in DataGenerator

**Labels:** `security`, `code-quality`, `P2-medium`

**Description:**
```markdown
## Problem
`DataGenerator` accepts user input without validation:
- `num_records` can be negative or extremely large
- `seed` can be any value
- YAML config structure not validated

## Impact
- Potential DoS through memory exhaustion
- Unexpected behavior with invalid inputs
- Poor error messages
- Security risk

## Proposed Solution

Add input validation methods:

```python
def _validate_num_records(self, num_records: int) -> int:
    """
    Validate number of records to generate.
    
    Args:
        num_records: Requested number of records
        
    Returns:
        Validated number of records
        
    Raises:
        ValueError: If num_records is invalid
    """
    if not isinstance(num_records, int):
        raise TypeError(f"num_records must be int, got {type(num_records)}")
    
    if num_records < 1:
        raise ValueError("num_records must be at least 1")
    
    if num_records > 10_000_000:
        raise ValueError(
            f"num_records={num_records} exceeds maximum limit of 10,000,000\n"
            "Consider generating data in batches for large datasets."
        )
    
    return num_records

def _validate_config(self, config: Dict[str, Any]) -> None:
    """
    Validate YAML configuration structure.
    
    Args:
        config: Loaded configuration dictionary
        
    Raises:
        ValueError: If configuration is invalid
    """
    required_keys = ['data_generation', 'fields']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    if not isinstance(config['fields'], list):
        raise ValueError("Configuration 'fields' must be a list")
    
    for field in config['fields']:
        required_field_keys = ['name', 'type', 'values']
        for key in required_field_keys:
            if key not in field:
                raise ValueError(
                    f"Field missing required key '{key}': {field}"
                )
```

## Tasks
- [ ] Add `_validate_num_records()` method
- [ ] Add `_validate_config()` method
- [ ] Add `_validate_seed()` method if needed
- [ ] Call validation methods in `__init__()`
- [ ] Add tests for validation methods
- [ ] Add tests for edge cases (negative, zero, very large)
- [ ] Update docstrings with validation information

## Validation Rules
- `num_records`: Must be 1 <= n <= 10,000,000
- `seed`: Must be non-negative integer if provided
- Config must have required keys: 'data_generation', 'fields'
- Each field must have: 'name', 'type', 'values'

## References
- PROJECT_REVIEW.md Issue #9
```

**Assignee:** Any contributor  
**Milestone:** v0.3.0

---

### Issue 10: Add Comprehensive Docstrings to All Modules

**Title:** Complete docstring coverage following PEP 257

**Labels:** `documentation`, `code-quality`, `P2-medium`, `good first issue`

**Description:**
```markdown
## Problem
Several functions and modules lack docstrings:
- `infra/logging_config.py` - Missing module and class docstrings
- `SQl_answer.py` - Missing function docstrings
- Various helper methods lack documentation

## Impact
- Harder for new contributors to understand code
- Poor IDE documentation support
- Not following PEP 257
- Difficult to generate API documentation

## Docstring Style
Use Google-style docstrings:

```python
def function_name(param1: str, param2: int = 10) -> bool:
    """
    One-line summary of function.
    
    More detailed description of what the function does,
    if needed. Can span multiple lines.
    
    Args:
        param1: Description of param1
        param2: Description of param2, defaults to 10
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input is provided
        FileNotFoundError: When file doesn't exist
        
    Examples:
        >>> function_name("test", 5)
        True
    """
    pass
```

## Tasks
- [ ] Add module docstrings to all Python files
- [ ] Add class docstrings with Attributes section
- [ ] Add method docstrings with Args, Returns, Raises
- [ ] Add docstrings to `infra/logging_config.py`
- [ ] Add docstrings to `SQl_answer.py`
- [ ] Review existing docstrings for completeness
- [ ] Add examples in docstrings where helpful
- [ ] Run docstring linter: `pydocstyle infra/`
- [ ] Generate API docs with sphinx to verify

## Example: logging_config.py

```python
"""
Logging configuration module for SQL Practice Platform.

This module provides centralized logging configuration for the platform,
ensuring consistent log formatting and file handling across all components.
"""

class LoggerManager:
    """
    Manages logging configuration for the SQL practice platform.
    
    This class creates and configures loggers with appropriate handlers
    and formatters for different components of the platform.
    
    Attributes:
        question_name: Optional name of the current question being evaluated
        log_dir: Directory where log files are stored
        formatters: Dictionary of available log formatters
    
    Examples:
        >>> manager = LoggerManager(question_name="sql_basic_select")
        >>> logger = manager.create_logger("validator")
        >>> logger.info("Starting validation")
    """
    
    def __init__(self, question_name: Optional[str] = None) -> None:
        """
        Initialize the LoggerManager.
        
        Args:
            question_name: Name of the question to include in log file name.
                          If None, uses generic log file name.
        """
        ...
```

## References
- PROJECT_REVIEW.md Issue #10
- PEP 257: https://www.python.org/dev/peps/pep-0257/
- Google Style Guide: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
```

**Assignee:** Documentation-focused contributor  
**Milestone:** v0.3.0

---

### Issue 11: Fix README Quick Start Guide

**Title:** Update README.md Quick Start to reflect actual usage

**Labels:** `documentation`, `P2-medium`, `good first issue`

**Description:**
```markdown
## Problem
The README.md Quick Start guide shows commands that don't work:

```bash
# From README
python SQl_answer.py sql_basic_select
```

But `SQl_answer.py` doesn't accept command-line arguments in its current implementation.

## Impact
- New users cannot follow quick start guide
- Poor first-time user experience
- Misleading documentation
- Frustration for contributors

## Current README Quick Start
```bash
# Clone the repository
git clone https://github.com/your-org/Practic_Questions_Platform.git
cd Practic_Questions_Platform

# Install dependencies
pip install -r requirements.txt

# Generate test data
python -m infra.DataGenerator

# Solve a question
python SQl_answer.py sql_basic_select  # ← This doesn't work!
```

## Proposed Fix

Option 1: Update README to reflect current behavior
```bash
# Install dependencies (after fixing requirements.txt)
pip install -r requirements.txt

# Run the platform (generates data and validates all active questions)
python SQl_answer.py
```

Option 2: Add CLI argument support to SQl_answer.py
```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="SQL Practice Questions Platform"
    )
    parser.add_argument(
        'question',
        nargs='?',
        help='Specific question to solve (optional)'
    )
    parser.add_argument(
        '--generate-only',
        action='store_true',
        help='Only generate test data, do not validate'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Generate initial data
    if not args.generate_only:
        data_gen = DataGenerator(yaml_config='infra/config/config.yml')
        data_gen.generate_records()
        data_gen.write_to_csv()
        data_gen.save_to_sqlite()
    
    # ... rest of logic
```

## Tasks
- [ ] Decide on Option 1 or Option 2
- [ ] Update README.md Quick Start section
- [ ] Test all commands in README
- [ ] Add troubleshooting section if needed
- [ ] Add example output for each command
- [ ] Update Docker usage examples if needed
- [ ] Ensure prerequisites are accurate

## Additional README Improvements
- [ ] Add actual repository URL (currently shows placeholder)
- [ ] Add screenshots or example output
- [ ] Add FAQ section
- [ ] Add troubleshooting guide

## References
- PROJECT_REVIEW.md Issue #11
```

**Assignee:** Documentation-focused contributor  
**Milestone:** v0.2.0

---

### Issue 12: Add YAML Configuration Validation

**Title:** Implement schema validation for YAML configuration files

**Labels:** `enhancement`, `configuration`, `P2-medium`

**Description:**
```markdown
## Problem
YAML configuration files (`config.yml`, `questions_config.yml`) are loaded but not validated against a schema. Invalid configurations cause runtime errors with poor error messages.

## Impact
- Invalid config causes runtime errors
- Poor error messages when config is wrong
- Hard to debug configuration issues
- No validation feedback for contributors

## Proposed Solution

Add JSON Schema validation for YAML configs:

```python
import jsonschema
from jsonschema import validate, ValidationError

# Schema for config.yml
CONFIG_SCHEMA = {
    "type": "object",
    "required": ["data_generation", "fields"],
    "properties": {
        "data_generation": {
            "type": "object",
            "required": ["num_records", "seed", "table_name"],
            "properties": {
                "num_records": {"type": "integer", "minimum": 1},
                "seed": {"type": "integer", "minimum": 0"},
                "table_name": {"type": "string", "minLength": 1}
            }
        },
        "fields": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["name", "type", "values"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"enum": ["int", "str", "bool"]},
                    "values": {}  # Depends on type
                }
            }
        }
    }
}

# Schema for questions_config.yml
QUESTIONS_CONFIG_SCHEMA = {
    "type": "object",
    "required": ["questions"],
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "difficulty", "active"],
                "properties": {
                    "name": {"type": "string"},
                    "difficulty": {
                        "enum": ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"]
                    },
                    "time_limit_seconds": {"type": "integer", "minimum": 60},
                    "hints_available": {"type": "integer", "minimum": 0},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "active": {"type": "boolean"}
                }
            }
        }
    }
}

def load_and_validate_config(yaml_file: Path, schema: dict) -> dict:
    """
    Load and validate YAML configuration.
    
    Args:
        yaml_file: Path to YAML file
        schema: JSON schema for validation
        
    Returns:
        Validated configuration dictionary
        
    Raises:
        ValidationError: If configuration doesn't match schema
    """
    with open(yaml_file) as f:
        config = yaml.safe_load(f)
    
    try:
        validate(instance=config, schema=schema)
    except ValidationError as e:
        raise ValueError(
            f"Invalid configuration in {yaml_file}:\n"
            f"{e.message}\n"
            f"Path: {' -> '.join(str(p) for p in e.path)}"
        )
    
    return config
```

## Tasks
- [ ] Create `infra/config/schemas.py` with JSON schemas
- [ ] Add jsonschema to requirements.txt
- [ ] Update `DataGenerator.load_yaml_config()` to validate
- [ ] Update question loading to validate questions_config.yml
- [ ] Add unit tests for schema validation
- [ ] Add tests for invalid configurations
- [ ] Document configuration format in docs/
- [ ] Add example configurations with comments

## Example Error Message
```
Invalid configuration in config.yml:
'num_records' is a required property
Path: data_generation -> num_records
```

## References
- PROJECT_REVIEW.md Issue #16
- JSON Schema: https://json-schema.org/
```

**Assignee:** Any contributor  
**Milestone:** v0.4.0

---

## Low Priority Issues (P3)

### Issue 13: Remove Commented Code from SQl_answer.py

**Title:** Clean up commented code in SQl_answer.py

**Labels:** `cleanup`, `P3-low`, `good first issue`

**Description:**
```markdown
## Problem
Large blocks of commented-out code exist in `SQl_answer.py` (lines 77-95).

## Impact
- Code clutter
- Confusion about intended functionality
- Harder to maintain

## Location
File: `SQl_answer.py`, lines 77-95

```python
    # # Basic usage
    # validator = AnswerValidator(question_name='sql_basic_select')
    # validator.load_sql()
    # validator.execute_query()
    # is_correct = validator.validate_answer()

    # # Print additional details
    # if is_correct:
    #     print("Solution is correct!")
    # else:
    #     print("Solution needs improvement")
    
    # ... more commented code
```

## Solution
1. Remove commented code
2. If examples are useful, move to:
   - `examples/` directory
   - Documentation
   - Docstrings

## Tasks
- [ ] Remove commented code from lines 77-95
- [ ] Check if examples should be preserved
- [ ] If yes, create `examples/basic_usage.py`
- [ ] Update documentation to reference examples
- [ ] Verify code still works after removal

## References
- PROJECT_REVIEW.md Issue #6
```

**Assignee:** Any contributor  
**Milestone:** v0.4.0

---

### Issue 14: Rename SQl_answer.py to Follow PEP 8

**Title:** Rename SQl_answer.py to sql_answer.py for PEP 8 compliance

**Labels:** `refactoring`, `P3-low`, `good first issue`

**Description:**
```markdown
## Problem
File name `SQl_answer.py` uses inconsistent capitalization. Should follow PEP 8 convention of lowercase with underscores.

## Current Name
```
SQl_answer.py
```

## Proposed Name
```
sql_answer.py
```

## Impact
- Not following PEP 8 naming conventions
- Minor confusion for contributors
- Inconsistent with other file names

## Tasks
- [ ] Rename `SQl_answer.py` to `sql_answer.py`
- [ ] Update all import statements (if any)
- [ ] Update README.md references
- [ ] Update Dockerfile COPY command (line 42)
- [ ] Update docker-compose.yml if referenced
- [ ] Update any documentation mentioning the file
- [ ] Test that everything still works

## Files to Update
- `Dockerfile` line 42
- `README.md` (multiple references)
- `docker-compose.yml` (check if referenced)
- Any other documentation

## Git Command
```bash
git mv SQl_answer.py sql_answer.py
```

## References
- PROJECT_REVIEW.md Issue #7
- PEP 8: https://www.python.org/dev/peps/pep-0008/#package-and-module-names
```

**Assignee:** Any contributor  
**Milestone:** v0.4.0

---

### Issue 15: Fix Documentation Folder Reference in README

**Title:** Update README.md folder name reference (solutions vs Sloutions)

**Labels:** `documentation`, `P3-low`, `good first issue`

**Description:**
```markdown
## Problem
README.md line 104 mentions a typo in folder naming that doesn't appear to exist:

```markdown
│       └── Sloutions/           # Note: typo to be fixed (see TASK-011)
```

However, the actual folder is named `solutions` (correct spelling).

## Investigation Needed
1. Check if "Sloutions" folder exists anywhere in the project
2. Verify actual folder structure matches documentation
3. Remove incorrect comment if folder is correctly named

## Tasks
- [ ] Search for any folders named "Sloutions": `find . -type d -name "*lout*"`
- [ ] Verify `Questions/*/solutions/` all use correct spelling
- [ ] If all folders are correct, update README.md line 104
- [ ] If typo exists, create issue to fix folder names
- [ ] Remove reference to non-existent TASK-011

## Expected Fix

If folders are correctly named:
```markdown
│       └── solutions/           # Expected output CSV files
```

If typo exists:
```bash
# Rename all misnamed folders
find Questions -type d -name "Sloutions" -exec bash -c 'mv "$0" "${0/Sloutions/solutions}"' {} \;
```

## References
- PROJECT_REVIEW.md Issue #14
- README.md line 104
```

**Assignee:** Any contributor  
**Milestone:** v0.4.0

---

## Summary

### Priority Breakdown
- **P0 (Critical):** 2 issues - Fix immediately
- **P1 (High):** 4 issues - Complete in next sprint
- **P2 (Medium):** 7 issues - Complete within 2-3 sprints
- **P3 (Low):** 3 issues - Complete as time permits

### Recommended Implementation Order
1. Fix requirements.txt (P0 - Quick win)
2. Add SQL query validation (P0 - Security)
3. Create requirements-dev.txt (P1 - Foundation)
4. Setup CI/CD pipeline (P1 - Automation)
5. Add test coverage (P1 - Quality)
6. Continue with P2 and P3 issues

### Estimated Total Effort
- P0: 4-6 hours
- P1: 12-16 hours
- P2: 20-24 hours
- P3: 4-6 hours
- **Total: 40-52 hours**

---

*This document should be used to create GitHub issues. Each issue template above can be copied directly into GitHub's issue creation form.*
