# Coding Standards & Quality Guidelines

This document outlines the coding standards and quality guidelines for all contributors, including AI agents, working on the SQL Practice Questions Platform.

## Table of Contents

1. [Python Style Guide](#python-style-guide)
2. [Code Structure](#code-structure)
3. [Documentation Standards](#documentation-standards)
4. [Testing Requirements](#testing-requirements)
5. [Git Workflow](#git-workflow)
6. [Security Guidelines](#security-guidelines)
7. [Performance Considerations](#performance-considerations)

---

## Python Style Guide

### General Principles

- Follow **PEP 8** style guidelines
- Use **PEP 257** docstring conventions
- Maximum line length: **88 characters** (Black formatter default)
- Use **4 spaces** for indentation (no tabs)

### Import Organization

```python
# Standard library imports
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Union

# Third-party imports
import pandas as pd
import yaml
from fastapi import FastAPI, HTTPException

# Local imports
from infra.validators import AnswerValidator
from infra.difficulty import DifficultyLevel
```

### Type Hints

All public methods and functions **must** include type hints:

```python
def validate_answer(
    self,
    user_query: str,
    expected_output: pd.DataFrame,
    tolerance: float = 0.0
) -> bool:
    """Validate user's SQL answer against expected output."""
    pass

def get_questions_by_difficulty(
    difficulty: DifficultyLevel,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Retrieve questions filtered by difficulty level."""
    pass
```

### Class Definitions

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class DifficultyLevel(Enum):
    """Enumeration of SQL question difficulty levels."""
    
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


@dataclass
class QuestionConfig:
    """Configuration for a SQL practice question.
    
    Attributes:
        name: Unique identifier for the question
        difficulty: Difficulty level of the question
        time_limit: Maximum time in seconds
        tags: List of topic tags
    """
    
    name: str
    difficulty: DifficultyLevel
    time_limit: int
    tags: List[str]
    prerequisite_questions: Optional[List[str]] = None


class AnswerValidator:
    """Validates user SQL answers against expected solutions.
    
    This class handles loading SQL queries, executing them against
    the practice database, and comparing results with expected output.
    
    Attributes:
        db_path: Path to the SQLite database
        question_name: Name of the current question
        
    Example:
        >>> validator = AnswerValidator(question_name='sql_basic_select')
        >>> validator.load_sql()
        >>> validator.execute_query()
        >>> is_correct = validator.validate_answer()
    """
    
    def __init__(
        self,
        question_name: str,
        base_dir: Optional[Path] = None
    ) -> None:
        """Initialize the AnswerValidator.
        
        Args:
            question_name: Name of the question to validate
            base_dir: Base directory of the project. Defaults to
                     parent of the current file.
                     
        Raises:
            ValueError: If question_name is not provided
            FileNotFoundError: If question directory doesn't exist
        """
        pass
```

### Error Handling

```python
# Use specific exception types
class QuestionNotFoundError(Exception):
    """Raised when a question cannot be found."""
    pass


class ValidationError(Exception):
    """Raised when answer validation fails."""
    pass


# Proper exception handling
def load_question(question_name: str) -> Dict[str, Any]:
    """Load question configuration.
    
    Args:
        question_name: Name of the question to load
        
    Returns:
        Dictionary containing question configuration
        
    Raises:
        QuestionNotFoundError: If question doesn't exist
        yaml.YAMLError: If configuration file is invalid
    """
    try:
        with open(f"Questions/{question_name}/metadata.yml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise QuestionNotFoundError(
            f"Question '{question_name}' not found"
        )
```

### Logging

```python
import logging

# Get logger for module
logger = logging.getLogger(__name__)


def process_answer(answer: str) -> bool:
    """Process and validate an answer.
    
    Uses structured logging for debugging and monitoring.
    """
    logger.info(
        "Processing answer",
        extra={"answer_length": len(answer)}
    )
    
    try:
        result = validate(answer)
        logger.info("Answer validated successfully")
        return result
    except ValidationError as e:
        logger.warning(
            "Validation failed",
            extra={"error": str(e)}
        )
        raise
```

---

## Code Structure

### Project Layout

```
practic_questions_platform/
├── infra/                    # Core infrastructure
│   ├── __init__.py
│   ├── validators.py         # Answer validation logic
│   ├── generators.py         # Data generation
│   ├── difficulty.py         # Difficulty system
│   └── ai/                   # AI integration
│       ├── __init__.py
│       ├── llama_client.py   # Llama model client
│       ├── hint_system.py    # Progressive hints
│       └── explainer.py      # Query explanations
├── api/                      # REST API
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── routes/              # API endpoints
│   └── models/              # Pydantic models
├── Questions/                # SQL questions
│   ├── beginner/
│   ├── intermediate/
│   └── advanced/
├── tests/                    # Test suite
│   ├── conftest.py
│   ├── test_validators.py
│   └── fixtures/
└── docs/                     # Documentation
```

### Module Organization

- One class per file for major components
- Related utilities can share a file
- Keep files under 500 lines
- Use `__init__.py` to expose public APIs

---

## Documentation Standards

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int = 10) -> bool:
    """Short one-line description.
    
    Longer description if needed. This can span multiple lines
    and should explain the function's purpose in detail.
    
    Args:
        param1: Description of param1. If it spans multiple
               lines, indent continuation lines.
        param2: Description of param2. Defaults to 10.
        
    Returns:
        Description of return value. For complex returns,
        describe the structure.
        
    Raises:
        ValueError: When param1 is empty.
        TypeError: When param2 is not an integer.
        
    Example:
        >>> result = function_name("test", 20)
        >>> print(result)
        True
        
    Note:
        Any additional notes about usage or behavior.
    """
    pass
```

### README Files

Each major component should have a README explaining:
- Purpose of the component
- How to use it
- Configuration options
- Examples

### Code Comments

```python
# Good: Explains WHY, not WHAT
# Using a tolerance of 0.01 because floating-point
# calculations may produce minor differences
if abs(result - expected) < 0.01:
    return True

# Bad: Explains WHAT (obvious from code)
# Check if result equals expected
if result == expected:
    return True
```

---

## Testing Requirements

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch

from infra.validators import AnswerValidator
from infra.difficulty import DifficultyLevel


class TestAnswerValidator:
    """Test suite for AnswerValidator class."""
    
    @pytest.fixture
    def validator(self, tmp_path):
        """Create a validator instance with test database."""
        # Setup test data
        db_path = tmp_path / "test.db"
        create_test_database(db_path)
        return AnswerValidator(db_path=db_path)
    
    @pytest.fixture
    def sample_query(self):
        """Sample SQL query for testing."""
        return "SELECT * FROM employees WHERE department = 'Sales'"
    
    def test_load_sql_valid_file(self, validator, tmp_path):
        """Test loading a valid SQL file."""
        # Arrange
        sql_file = tmp_path / "test.sql"
        sql_file.write_text("SELECT * FROM employees")
        
        # Act
        validator.load_sql(sql_file)
        
        # Assert
        assert validator.query == "SELECT * FROM employees"
    
    def test_load_sql_missing_file(self, validator):
        """Test handling of missing SQL file."""
        with pytest.raises(FileNotFoundError):
            validator.load_sql(Path("/nonexistent/file.sql"))
    
    def test_execute_query_success(self, validator, sample_query):
        """Test successful query execution."""
        validator.query = sample_query
        validator.execute_query()
        
        assert validator.answer_df is not None
        assert len(validator.answer_df) > 0
    
    @pytest.mark.parametrize("query,expected_count", [
        ("SELECT * FROM employees", 100),
        ("SELECT * FROM employees LIMIT 10", 10),
        ("SELECT * FROM employees WHERE 1=0", 0),
    ])
    def test_query_results_count(self, validator, query, expected_count):
        """Test query results with different row counts."""
        validator.query = query
        validator.execute_query()
        assert len(validator.answer_df) == expected_count
```

### Coverage Requirements

- Minimum **80%** code coverage
- **100%** coverage for critical paths (validation, scoring)
- All public APIs must have tests

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=infra --cov-report=html

# Run specific test file
pytest tests/test_validators.py -v

# Run tests matching pattern
pytest tests/ -v -k "test_validation"
```

---

## Git Workflow

### Branch Naming

```
feature/TASK-XXX-short-description
bugfix/TASK-XXX-short-description
docs/update-readme
refactor/improve-validator-performance
```

### Commit Messages

```
Format: <type>(<scope>): <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style (no logic change)
- refactor: Code refactoring
- test: Adding/updating tests
- chore: Maintenance

Examples:
feat(difficulty): add DifficultyLevel enum
fix(validator): handle empty query result
docs(readme): add installation instructions
test(generator): add edge case tests
refactor(user): extract progress tracking logic
```

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guide
- [ ] Type hints on all public methods
- [ ] Docstrings on all classes and public methods
- [ ] Unit tests added/updated
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] No linting errors (`flake8 infra/`)
- [ ] No type errors (`mypy infra/`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)

---

## Security Guidelines

### Input Validation

```python
# Always validate and sanitize user input
def execute_user_query(query: str, db_path: Path) -> pd.DataFrame:
    """Execute a user-provided SQL query safely.
    
    Uses parameterized queries where possible and validates
    input to prevent SQL injection.
    """
    # Validate query doesn't contain dangerous operations
    forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
    query_upper = query.upper()
    
    for keyword in forbidden_keywords:
        if keyword in query_upper:
            raise SecurityError(f"Forbidden operation: {keyword}")
    
    # Use read-only connection
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()
```

### Secrets Management

- Never commit secrets to the repository
- Use environment variables for sensitive configuration
- Document required environment variables in README

### File Operations

```python
from pathlib import Path

def safe_read_file(file_path: Path, base_dir: Path) -> str:
    """Read file contents safely, preventing path traversal.
    
    Args:
        file_path: Path to file to read
        base_dir: Base directory that file must be within
        
    Raises:
        SecurityError: If path traversal is detected
    """
    resolved_path = file_path.resolve()
    resolved_base = base_dir.resolve()
    
    # Ensure file is within allowed directory
    if not str(resolved_path).startswith(str(resolved_base)):
        raise SecurityError("Path traversal detected")
    
    return resolved_path.read_text()
```

---

## Performance Considerations

### Database Operations

```python
# Use connection pooling for frequent operations
from contextlib import contextmanager
import sqlite3

@contextmanager
def get_db_connection(db_path: Path):
    """Context manager for database connections."""
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


# Batch operations when possible
def insert_many_records(records: List[Dict], db_path: Path):
    """Insert multiple records efficiently."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO table_name VALUES (?, ?, ?)",
            [(r['a'], r['b'], r['c']) for r in records]
        )
        conn.commit()
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def load_question_config(question_name: str) -> Dict[str, Any]:
    """Load question configuration with caching."""
    # Configuration is read from disk once, then cached
    pass
```

### Lazy Loading

```python
class QuestionLoader:
    """Lazy-loading question manager."""
    
    def __init__(self):
        self._questions: Optional[Dict] = None
    
    @property
    def questions(self) -> Dict:
        """Lazy load questions on first access."""
        if self._questions is None:
            self._questions = self._load_all_questions()
        return self._questions
```

---

## AI Agent-Specific Guidelines

When AI agents work on this codebase, they should:

1. **Read existing code first** - Understand patterns before adding new code
2. **Make minimal changes** - Only modify what's necessary
3. **Maintain consistency** - Follow existing patterns in the codebase
4. **Test thoroughly** - Add tests for all new functionality
5. **Document clearly** - Include docstrings and comments
6. **Handle errors gracefully** - Use proper exception handling
7. **Consider security** - Validate all inputs
8. **Think about performance** - Avoid unnecessary operations

---

*Last Updated: November 2024*
