# SQL Practice Questions Platform - Product Roadmap

## Executive Summary

This roadmap outlines the strategic tasks needed to transform the SQL Practice Questions Platform into a comprehensive, multi-level learning platform with AI-powered assistance using local Llama models.

---

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Strategic Objectives](#strategic-objectives)
3. [Task Categories](#task-categories)
4. [Detailed Task List](#detailed-task-list)
5. [AI Agent Task Delegation](#ai-agent-task-delegation)
6. [Coding Standards & Quality Guidelines](#coding-standards--quality-guidelines)
7. [Implementation Phases](#implementation-phases)

---

## Current State Analysis

### Existing Capabilities
- Basic SQL query validation against SQLite database
- User progress tracking with JSON-based storage
- Question configuration via YAML files
- Logging infrastructure
- Single difficulty level (basic SELECT queries)

### Current Limitations
- No structured difficulty levels (beginner, intermediate, advanced, expert)
- Limited question types (only basic SELECT)
- No AI/LLM integration for hints or explanations
- No web interface
- Limited test coverage
- No API layer for future integrations

---

## Strategic Objectives

1. **Multi-Level SQL Practice Support**
   - Implement beginner, intermediate, advanced, and expert difficulty levels
   - Create diverse SQL question categories (SELECT, JOIN, subqueries, window functions, CTEs)

2. **Local Llama AI Integration**
   - Integrate local Llama models for intelligent hints
   - Provide AI-powered query explanations
   - Generate dynamic feedback on user solutions

3. **Platform Scalability**
   - RESTful API architecture
   - Database migration from SQLite to PostgreSQL support
   - Modular question and test framework

4. **Quality Assurance**
   - Comprehensive test coverage
   - Code documentation
   - CI/CD pipeline

---

## Task Categories

| Category | Priority | Estimated Effort |
|----------|----------|------------------|
| Core Infrastructure | High | 2-3 weeks |
| Difficulty Levels | High | 1-2 weeks |
| AI/LLM Integration | High | 2-3 weeks |
| Testing Framework | Medium | 1-2 weeks |
| API Development | Medium | 2-3 weeks |
| Documentation | Medium | 1 week |
| DevOps & CI/CD | Low | 1 week |

---

## Detailed Task List

### Phase 1: Core Infrastructure Enhancement

#### TASK-001: Refactor Project Structure
**Priority:** High  
**Estimated Time:** 4-6 hours  
**Assignee:** AI Agent - Infrastructure

**Description:**
Reorganize the project to follow Python best practices with proper packaging.

**Specific Instructions:**
```
1. Create a proper Python package structure:
   practic_questions_platform/
   ├── __init__.py
   ├── core/
   │   ├── __init__.py
   │   ├── validators.py
   │   ├── generators.py
   │   └── models.py
   ├── questions/
   │   ├── __init__.py
   │   └── loader.py
   ├── users/
   │   ├── __init__.py
   │   └── manager.py
   ├── ai/
   │   ├── __init__.py
   │   └── llama_client.py
   └── api/
       ├── __init__.py
       └── routes.py

2. Move existing code to appropriate modules
3. Update all import statements
4. Create setup.py or pyproject.toml for package installation
5. Ensure backward compatibility with existing functionality
```

**Acceptance Criteria:**
- [ ] Package structure follows PEP 8 conventions
- [ ] All existing tests pass
- [ ] Code can be installed via `pip install -e .`
- [ ] No breaking changes to existing functionality

---

#### TASK-002: Implement Difficulty Level System
**Priority:** High  
**Estimated Time:** 6-8 hours  
**Assignee:** AI Agent - Core Features

**Description:**
Create a comprehensive difficulty level system for SQL questions.

**Specific Instructions:**
```python
# Create infra/difficulty.py with the following structure:

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional

class DifficultyLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

@dataclass
class DifficultyConfig:
    level: DifficultyLevel
    time_limit_seconds: int
    hint_count: int
    allowed_sql_features: List[str]
    scoring_multiplier: float
    prerequisite_level: Optional[DifficultyLevel] = None

# Implement difficulty configurations for each level:
# - BEGINNER: Basic SELECT, WHERE, ORDER BY, LIMIT
# - INTERMEDIATE: JOINs, GROUP BY, HAVING, subqueries
# - ADVANCED: Window functions, CTEs, complex aggregations
# - EXPERT: Query optimization, recursive CTEs, advanced analytics

# Update questions_config.yml schema to include:
# - difficulty_level: BEGINNER | INTERMEDIATE | ADVANCED | EXPERT
# - time_limit: <seconds>
# - hints_available: <count>
# - prerequisite_questions: [list of question names]
# - sql_features: [list of allowed SQL features]
```

**Acceptance Criteria:**
- [ ] DifficultyLevel enum with 4 levels implemented
- [ ] DifficultyConfig dataclass with all required fields
- [ ] Updated questions_config.yml schema
- [ ] Validation logic for difficulty level progression
- [ ] Unit tests for difficulty system

---

#### TASK-003: Database Schema Enhancement
**Priority:** High  
**Estimated Time:** 4-6 hours  
**Assignee:** AI Agent - Database

**Description:**
Enhance the database schema to support more complex SQL questions.

**Specific Instructions:**
```sql
-- Create multiple related tables for JOIN practice:

-- employees table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    department_id INTEGER,
    manager_id INTEGER,
    hire_date DATE,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

-- departments table
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    location TEXT,
    budget DECIMAL(12,2)
);

-- projects table
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- employee_projects table (many-to-many)
CREATE TABLE employee_projects (
    employee_id INTEGER,
    project_id INTEGER,
    role TEXT,
    hours_allocated INTEGER,
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Update DataGenerator.py to:
1. Support multiple table generation
2. Maintain referential integrity
3. Generate realistic data distributions
```

**Acceptance Criteria:**
- [ ] Multi-table schema implemented
- [ ] Foreign key relationships defined
- [ ] DataGenerator updated for multiple tables
- [ ] Data integrity constraints enforced
- [ ] Migration script for existing installations

---

### Phase 2: AI/LLM Integration

#### TASK-004: Local Llama Integration Framework
**Priority:** High  
**Estimated Time:** 8-12 hours  
**Assignee:** AI Agent - AI/ML

**Description:**
Implement local Llama AI integration for intelligent SQL assistance.

**Specific Instructions:**
```python
# Create infra/ai/llama_client.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
import subprocess
import json

@dataclass
class LlamaConfig:
    model_path: str
    context_length: int = 4096
    temperature: float = 0.7
    max_tokens: int = 512
    top_p: float = 0.9

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def generate_hint(self, question: str, user_query: str, 
                     difficulty: str) -> str:
        pass
    
    @abstractmethod
    def explain_query(self, sql_query: str) -> str:
        pass
    
    @abstractmethod
    def analyze_error(self, user_query: str, error_message: str) -> str:
        pass
    
    @abstractmethod
    def suggest_optimization(self, sql_query: str) -> str:
        pass

class LocalLlamaClient(BaseLLMClient):
    """Client for local Llama model via llama.cpp or Ollama"""
    
    def __init__(self, config: LlamaConfig):
        self.config = config
        self._validate_model()
    
    def _validate_model(self) -> bool:
        """Check if model is available locally"""
        pass
    
    def _create_prompt(self, system_prompt: str, 
                       user_prompt: str) -> str:
        """Create properly formatted prompt for Llama"""
        pass
    
    def generate_hint(self, question: str, user_query: str,
                     difficulty: str) -> str:
        """Generate contextual hints based on difficulty level"""
        system_prompt = '''You are a SQL tutor. Provide hints without 
        giving away the complete solution. Adjust hint specificity 
        based on difficulty level.'''
        pass
    
    def explain_query(self, sql_query: str) -> str:
        """Explain SQL query in plain English"""
        pass
    
    def analyze_error(self, user_query: str, 
                     error_message: str) -> str:
        """Analyze SQL errors and provide guidance"""
        pass

# Support for multiple backends:
# 1. llama.cpp (direct binary)
# 2. Ollama (API-based)
# 3. llama-cpp-python (Python bindings)
```

**Acceptance Criteria:**
- [ ] Abstract LLM client interface defined
- [ ] LocalLlamaClient implementation complete
- [ ] Support for at least 2 backends (Ollama + llama-cpp-python)
- [ ] Configurable model parameters
- [ ] Error handling for model unavailability
- [ ] Unit tests with mock LLM responses

---

#### TASK-005: AI-Powered Hint System
**Priority:** High  
**Estimated Time:** 6-8 hours  
**Assignee:** AI Agent - AI/ML

**Description:**
Create an intelligent hint system that provides progressive hints based on difficulty level and user progress.

**Specific Instructions:**
```python
# Create infra/ai/hint_system.py

from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

class HintLevel(Enum):
    SUBTLE = 1      # Very indirect hint
    MODERATE = 2    # Points in right direction
    EXPLICIT = 3    # Nearly gives answer

@dataclass
class Hint:
    level: HintLevel
    content: str
    penalty_points: int

class ProgressiveHintSystem:
    """
    Provides hints that become more specific as user requests more.
    Tracks hint usage for scoring adjustments.
    """
    
    def __init__(self, llama_client, difficulty_level: str):
        self.llama_client = llama_client
        self.difficulty_level = difficulty_level
        self.hints_used: List[Hint] = []
        
    def get_next_hint(self, question: str, 
                      user_query: Optional[str] = None,
                      error_message: Optional[str] = None) -> Hint:
        """
        Generate next hint based on:
        - Current difficulty level
        - Number of hints already used
        - User's current query attempt
        - Any error messages
        """
        pass
    
    def calculate_hint_penalty(self) -> int:
        """Calculate total score penalty for hints used"""
        pass
    
    # Hint strategies per difficulty:
    # BEGINNER: 5 hints, generous, low penalty
    # INTERMEDIATE: 3 hints, moderate specificity
    # ADVANCED: 2 hints, subtle only
    # EXPERT: 1 hint, very subtle, high penalty
```

**Acceptance Criteria:**
- [ ] ProgressiveHintSystem class implemented
- [ ] Hint level progression logic
- [ ] Integration with LocalLlamaClient
- [ ] Scoring penalty calculation
- [ ] Configurable hint count per difficulty
- [ ] Unit tests for hint progression

---

#### TASK-006: Query Explanation Engine
**Priority:** Medium  
**Estimated Time:** 4-6 hours  
**Assignee:** AI Agent - AI/ML

**Description:**
Build an AI-powered SQL query explanation system.

**Specific Instructions:**
```python
# Create infra/ai/explainer.py

class SQLExplainer:
    """
    Provides detailed explanations of SQL queries using AI.
    Supports multiple explanation modes:
    - Step-by-step execution flow
    - Clause-by-clause breakdown
    - Performance implications
    - Alternative approaches
    """
    
    def __init__(self, llama_client):
        self.llama_client = llama_client
    
    def explain_step_by_step(self, query: str) -> List[str]:
        """Break down query into logical steps"""
        pass
    
    def explain_clauses(self, query: str) -> Dict[str, str]:
        """Explain each SQL clause individually"""
        pass
    
    def explain_for_beginner(self, query: str) -> str:
        """Simplified explanation for beginners"""
        pass
    
    def suggest_improvements(self, query: str) -> List[str]:
        """Suggest query optimizations"""
        pass

# Integrate with AnswerValidator to provide:
# - Explanation of expected solution
# - Comparison of user solution vs expected
# - Suggestions for improvement
```

**Acceptance Criteria:**
- [ ] SQLExplainer class with all explanation methods
- [ ] Integration with AnswerValidator
- [ ] Beginner-friendly explanations
- [ ] Performance suggestion capability
- [ ] Unit tests with sample queries

---

### Phase 3: Question Library Expansion

#### TASK-007: Create Beginner SQL Questions
**Priority:** High  
**Estimated Time:** 4-6 hours  
**Assignee:** AI Agent - Content

**Description:**
Create a comprehensive set of beginner-level SQL questions.

**Specific Instructions:**
```yaml
# Create Questions/beginner/ directory with 10 questions:

# Question categories:
1. basic_select_all - SELECT * FROM table
2. select_specific_columns - SELECT col1, col2 FROM table
3. where_equals - WHERE column = value
4. where_comparison - WHERE column > value
5. where_like - WHERE column LIKE pattern
6. order_by_single - ORDER BY column
7. order_by_multiple - ORDER BY col1, col2 DESC
8. limit_results - LIMIT n
9. distinct_values - SELECT DISTINCT
10. basic_count - SELECT COUNT(*)

# Each question folder must contain:
# - question.txt (detailed problem description)
# - example_solution.sql (reference solution)
# - solutions/solution_df.csv (expected output)
# - metadata.yml (difficulty, tags, hints, time_limit)

# Example metadata.yml:
difficulty: BEGINNER
time_limit_seconds: 300
hints_available: 5
tags:
  - select
  - where
  - beginner
prerequisite_questions: []
sql_features:
  - SELECT
  - WHERE
  - ORDER BY
learning_objectives:
  - Understand basic SELECT syntax
  - Filter data with WHERE clause
```

**Acceptance Criteria:**
- [ ] 10 beginner questions created
- [ ] Each question has complete folder structure
- [ ] metadata.yml for each question
- [ ] Solutions validated against test database
- [ ] Progressive difficulty within beginner level

---

#### TASK-008: Create Intermediate SQL Questions
**Priority:** High  
**Estimated Time:** 6-8 hours  
**Assignee:** AI Agent - Content

**Description:**
Create intermediate-level SQL questions focusing on JOINs and aggregations.

**Specific Instructions:**
```yaml
# Create Questions/intermediate/ directory with 15 questions:

# Question categories:
# JOINs (5 questions):
1. inner_join_basic - Basic INNER JOIN
2. left_join_basic - LEFT JOIN with NULL handling
3. multiple_table_join - Join 3+ tables
4. self_join - Self-referential JOIN
5. cross_join - Cartesian product understanding

# Aggregations (5 questions):
6. group_by_count - GROUP BY with COUNT
7. group_by_sum - GROUP BY with SUM
8. group_by_avg - GROUP BY with AVG
9. having_clause - HAVING filter on aggregates
10. multiple_aggregates - Multiple aggregate functions

# Subqueries (5 questions):
11. subquery_where - Subquery in WHERE clause
12. subquery_from - Subquery in FROM clause
13. correlated_subquery - Correlated subquery
14. exists_clause - EXISTS subquery
15. in_subquery - IN with subquery

# Prerequisite requirements:
- All intermediate questions require completion of 
  at least 7 beginner questions
```

**Acceptance Criteria:**
- [ ] 15 intermediate questions created
- [ ] Complete folder structure for each
- [ ] Proper prerequisite chain
- [ ] Multi-table queries using enhanced schema
- [ ] Solutions validated

---

#### TASK-009: Create Advanced SQL Questions
**Priority:** Medium  
**Estimated Time:** 6-8 hours  
**Assignee:** AI Agent - Content

**Description:**
Create advanced SQL questions covering window functions and CTEs.

**Specific Instructions:**
```yaml
# Create Questions/advanced/ directory with 10 questions:

# Window Functions (5 questions):
1. row_number - ROW_NUMBER() OVER()
2. rank_dense_rank - RANK() vs DENSE_RANK()
3. lead_lag - LEAD() and LAG() functions
4. running_total - SUM() OVER (ORDER BY)
5. partition_by - PARTITION BY clause

# Common Table Expressions (5 questions):
6. basic_cte - Simple WITH clause
7. multiple_cte - Multiple CTEs
8. recursive_cte_simple - Basic recursive CTE
9. recursive_cte_hierarchy - Hierarchical data
10. cte_with_window - CTE combined with window functions

# Each question should include:
- Detailed explanation of the concept
- Multiple test cases
- Performance considerations
- Real-world use case example
```

**Acceptance Criteria:**
- [ ] 10 advanced questions created
- [ ] Window function questions complete
- [ ] CTE questions with recursion
- [ ] Clear prerequisite requirements
- [ ] Performance notes included

---

### Phase 4: Testing & Quality Assurance

#### TASK-010: Implement Comprehensive Test Suite
**Priority:** High  
**Estimated Time:** 8-10 hours  
**Assignee:** AI Agent - Testing

**Description:**
Create a comprehensive test suite covering all platform functionality.

**Specific Instructions:**
```python
# Create tests/ directory with pytest structure:

tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_validators.py       # AnswerValidator tests
├── test_generators.py       # DataGenerator tests
├── test_user_system.py      # User management tests
├── test_difficulty.py       # Difficulty system tests
├── test_ai_integration.py   # AI/LLM integration tests
├── test_question_loader.py  # Question loading tests
└── fixtures/
    ├── sample_questions/
    └── sample_data/

# Test coverage requirements:
# - Unit tests for all classes and methods
# - Integration tests for database operations
# - Mock tests for AI/LLM functionality
# - Edge case coverage
# - Error handling tests

# Example test structure:
import pytest
from infra.AnswerValidator import AnswerValidator
from infra.difficulty import DifficultyLevel, DifficultyConfig

class TestAnswerValidator:
    @pytest.fixture
    def validator(self, tmp_path):
        """Create validator with test database"""
        pass
    
    def test_load_sql_valid_file(self, validator):
        """Test loading valid SQL file"""
        pass
    
    def test_load_sql_invalid_file(self, validator):
        """Test handling of invalid SQL file"""
        pass
    
    def test_execute_query_success(self, validator):
        """Test successful query execution"""
        pass
    
    def test_validate_answer_correct(self, validator):
        """Test validation of correct answer"""
        pass
    
    def test_validate_answer_incorrect(self, validator):
        """Test validation of incorrect answer"""
        pass

# Run with: pytest tests/ -v --cov=infra --cov-report=html
```

**Acceptance Criteria:**
- [ ] pytest test suite structure created
- [ ] 80%+ code coverage
- [ ] All existing functionality covered
- [ ] CI/CD integration ready
- [ ] Documentation for running tests

---

#### TASK-011: Fix Existing Code Issues
**Priority:** High  
**Estimated Time:** 4-6 hours  
**Assignee:** AI Agent - Code Quality

**Description:**
Fix identified issues in existing codebase.

**Specific Instructions:**
```python
# Known issues to fix:

# 1. Missing import in user.py (line 54)
#    Add: from datetime import datetime

# 2. Typo in folder names: "sloutions" should be "solutions"
#    Update all references in code and folder names

# 3. Inconsistent path handling
#    Standardize on pathlib.Path throughout

# 4. Missing error handling in DataGenerator
#    Add proper exception handling for file operations

# 5. SQL injection vulnerability potential
#    Review query building and add parameterization

# 6. Logging configuration improvements
#    Avoid duplicate handlers, add log rotation

# 7. Type hints missing throughout codebase
#    Add proper type annotations

# 8. requirements.txt cleanup
#    - uuid is part of stdlib, remove
#    - logging is part of stdlib, remove
#    - Add missing dependencies (sqlite3 is stdlib)
#    - Add version constraints
```

**Acceptance Criteria:**
- [ ] All identified issues fixed
- [ ] No breaking changes
- [ ] Type hints added to public APIs
- [ ] Code passes flake8/pylint
- [ ] Updated requirements.txt

---

### Phase 5: API Development

#### TASK-012: RESTful API Framework
**Priority:** Medium  
**Estimated Time:** 8-10 hours  
**Assignee:** AI Agent - Backend

**Description:**
Create a RESTful API for the platform using FastAPI.

**Specific Instructions:**
```python
# Create api/ directory with FastAPI structure:

api/
├── __init__.py
├── main.py              # FastAPI app initialization
├── routes/
│   ├── __init__.py
│   ├── questions.py     # Question endpoints
│   ├── users.py         # User endpoints
│   ├── validation.py    # Answer validation endpoints
│   └── ai.py           # AI assistance endpoints
├── models/
│   ├── __init__.py
│   ├── request.py       # Pydantic request models
│   └── response.py      # Pydantic response models
└── middleware/
    ├── __init__.py
    └── auth.py          # Authentication middleware

# API Endpoints:

# Questions
GET  /api/v1/questions              # List all questions
GET  /api/v1/questions/{id}         # Get question details
GET  /api/v1/questions/difficulty/{level}  # Filter by difficulty

# Users
POST /api/v1/users                  # Create user
GET  /api/v1/users/{id}             # Get user profile
GET  /api/v1/users/{id}/progress    # Get user progress

# Validation
POST /api/v1/validate               # Validate SQL answer
{
    "question_id": "sql_basic_select",
    "user_query": "SELECT * FROM employees",
    "user_id": "user123"
}

# AI Assistance
POST /api/v1/ai/hint               # Get AI hint
POST /api/v1/ai/explain            # Explain query
POST /api/v1/ai/analyze-error      # Analyze error

# Add to requirements.txt:
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0
```

**Acceptance Criteria:**
- [ ] FastAPI application structure created
- [ ] All endpoints documented with OpenAPI
- [ ] Request/response models with validation
- [ ] Error handling middleware
- [ ] API tests with pytest
- [ ] Swagger UI accessible at /docs

---

### Phase 6: Documentation & DevOps

#### TASK-013: Comprehensive Documentation
**Priority:** Medium  
**Estimated Time:** 4-6 hours  
**Assignee:** AI Agent - Documentation

**Description:**
Create comprehensive project documentation.

**Specific Instructions:**
```markdown
# Create/update the following documentation:

# 1. README.md - Complete overhaul
- Project overview and features
- Quick start guide
- Installation instructions
- Usage examples
- API documentation link
- Contributing guidelines

# 2. docs/architecture.md
- System architecture diagram
- Component descriptions
- Data flow diagrams
- Database schema documentation

# 3. docs/api.md
- API endpoint documentation
- Request/response examples
- Authentication guide
- Error codes

# 4. docs/contributing.md
- Code style guide
- Branch naming conventions
- Pull request process
- Testing requirements

# 5. docs/ai-integration.md
- Llama setup instructions
- Supported models
- Configuration options
- Troubleshooting guide

# 6. CHANGELOG.md
- Version history
- Feature additions
- Bug fixes
- Breaking changes
```

**Acceptance Criteria:**
- [ ] README.md completely updated
- [ ] All documentation files created
- [ ] Code examples in documentation
- [ ] Screenshots where applicable
- [ ] Links between documents

---

#### TASK-014: CI/CD Pipeline
**Priority:** Medium  
**Estimated Time:** 4-6 hours  
**Assignee:** AI Agent - DevOps

**Description:**
Set up continuous integration and deployment pipeline.

**Specific Instructions:**
```yaml
# Create .github/workflows/ci.yml

name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install flake8 pylint black isort
      - name: Run linters
        run: |
          flake8 infra/ api/ tests/
          black --check infra/ api/ tests/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt
      - name: Run tests
        run: pytest tests/ -v --cov=infra --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security scan
        uses: pyupio/safety@v1

# Create requirements-dev.txt:
pytest>=7.0.0
pytest-cov>=4.0.0
flake8>=6.0.0
black>=23.0.0
isort>=5.12.0
mypy>=1.0.0
```

**Acceptance Criteria:**
- [ ] CI workflow file created
- [ ] Linting stage working
- [ ] Testing stage with coverage
- [ ] Security scanning included
- [ ] Branch protection rules documented

---

## AI Agent Task Delegation

### GitHub Issue Templates

Create issues using these templates to delegate tasks to AI agents:

#### Issue Template: Feature Implementation
```markdown
## Task: [TASK-XXX] - [Task Title]

### Description
[Detailed description from task list above]

### Specific Instructions
[Copy specific instructions from task]

### Acceptance Criteria
[Copy acceptance criteria checkboxes]

### Technical Requirements
- Python version: 3.10+
- Follow PEP 8 style guide
- Include type hints
- Write unit tests
- Update documentation

### AI Agent Instructions
1. Read and understand the full task description
2. Review existing code in the repository
3. Implement changes following the specific instructions
4. Write comprehensive tests
5. Update any affected documentation
6. Create a pull request with detailed description

### Labels
- enhancement
- ai-agent-task
- [priority label: P0/P1/P2]
- [component label: infrastructure/ai/content/testing]
```

#### Issue Template: Bug Fix
```markdown
## Bug: [Description]

### Current Behavior
[What happens now]

### Expected Behavior
[What should happen]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]

### Technical Details
- File(s) affected: [list files]
- Error message: [if applicable]

### AI Agent Instructions
1. Reproduce the bug locally
2. Identify root cause
3. Implement fix with minimal changes
4. Add regression test
5. Verify fix doesn't break other functionality
```

---

## Coding Standards & Quality Guidelines

### For AI Agents Working on This Project

#### Python Style Guide
```python
# Follow PEP 8 with these specifics:

# Imports
from typing import List, Dict, Optional, Any
import stdlib_modules
import third_party_modules
import local_modules

# Class definitions
class ClassName:
    """
    Docstring describing the class.
    
    Attributes:
        attr1: Description of attr1
        attr2: Description of attr2
    """
    
    def method_name(self, param1: str, param2: int = 10) -> bool:
        """
        One-line description.
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When invalid input is provided
        """
        pass

# Use dataclasses for data containers
@dataclass
class DataContainer:
    field1: str
    field2: int
    field3: Optional[List[str]] = None

# Use enums for fixed choices
class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
```

#### Testing Standards
```python
# Use pytest with fixtures
import pytest

class TestFeatureName:
    """Tests for FeatureName functionality."""
    
    @pytest.fixture
    def setup_data(self):
        """Create test data."""
        return {"key": "value"}
    
    def test_normal_case(self, setup_data):
        """Test normal operation."""
        result = function_under_test(setup_data)
        assert result == expected_value
    
    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            function_under_test(invalid_input)
    
    def test_error_handling(self):
        """Test error conditions."""
        pass
```

#### Git Commit Messages
```
Format: <type>(<scope>): <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style (formatting, no logic change)
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance tasks

Examples:
- feat(difficulty): add DifficultyLevel enum and config
- fix(validator): handle missing solution file gracefully
- docs(readme): update installation instructions
- test(generator): add unit tests for DataGenerator
```

#### Pull Request Checklist
```markdown
## PR Checklist

- [ ] Code follows project style guide
- [ ] Type hints added for all public methods
- [ ] Docstrings added for all classes and public methods
- [ ] Unit tests added/updated
- [ ] All tests pass locally
- [ ] No linting errors (flake8/pylint)
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented in PR)
```

---

## Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
- [x] TASK-011: Fix existing code issues
- [ ] TASK-001: Refactor project structure
- [ ] TASK-002: Implement difficulty level system
- [ ] TASK-003: Database schema enhancement

### Phase 2: AI Integration (Weeks 3-4)
- [ ] TASK-004: Local Llama integration framework
- [ ] TASK-005: AI-powered hint system
- [ ] TASK-006: Query explanation engine

### Phase 3: Content Expansion (Weeks 5-6)
- [ ] TASK-007: Create beginner SQL questions
- [ ] TASK-008: Create intermediate SQL questions
- [ ] TASK-009: Create advanced SQL questions

### Phase 4: Quality & API (Weeks 7-8)
- [ ] TASK-010: Implement comprehensive test suite
- [ ] TASK-012: RESTful API framework
- [ ] TASK-013: Comprehensive documentation
- [ ] TASK-014: CI/CD pipeline

---

## Getting Started for AI Agents

1. **Clone the repository** and review the existing code structure
2. **Read this roadmap** thoroughly before starting any task
3. **Check the task dependencies** - some tasks require others to be completed first
4. **Follow the coding standards** outlined in this document
5. **Create detailed PRs** with descriptions matching the task acceptance criteria
6. **Run tests locally** before submitting any PR
7. **Ask questions** if any requirements are unclear

---

## Contact & Support

For questions about this roadmap or task clarification, create a GitHub issue with the label `question`.

---

*Last Updated: November 2024*
*Version: 1.0*
