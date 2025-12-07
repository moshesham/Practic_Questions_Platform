#!/bin/bash
# Script to create GitHub issues from ISSUES_TO_CREATE.md templates
# This script requires the GitHub CLI (gh) to be installed and authenticated

set -e

REPO="moshesham/Practic_Questions_Platform"

echo "Creating GitHub issues for $REPO..."
echo ""

# Issue 1: Fix requirements.txt
echo "Creating Issue #1: Fix requirements.txt..."
gh issue create \
  --repo "$REPO" \
  --title "Fix requirements.txt - Remove stdlib modules and add version constraints" \
  --label "bug,dependencies,P0-critical,good first issue" \
  --milestone "v0.2.0" \
  --body "## Problem
The \`requirements.txt\` file contains Python standard library modules that should not be listed as dependencies:
- \`uuid\` (line 3)
- \`logging\` (line 4)

Additionally, dependencies lack version constraints which can lead to breaking changes and inconsistent behavior across environments.

## Current State
\`\`\`txt
pandas
pyyaml
uuid
logging
\`\`\`

## Expected State
\`\`\`txt
pandas>=2.0.0,<3.0.0
pyyaml>=6.0,<7.0
\`\`\`

## Impact
- Confusing for new contributors
- May cause installation issues with some package managers
- Unpredictable behavior across different installations
- Potential security vulnerabilities from outdated packages

## Tasks
- [ ] Remove \`uuid\` from requirements.txt
- [ ] Remove \`logging\` from requirements.txt
- [ ] Add version constraint to \`pandas\` (>=2.0.0,<3.0.0)
- [ ] Add version constraint to \`pyyaml\` (>=6.0,<7.0)
- [ ] Test installation with updated requirements

## References
- See PROJECT_REVIEW.md Issue #1 and #2
- Related PRODUCT_ROADMAP.md TASK-011"

echo "✓ Issue #1 created"
echo ""

# Issue 2: SQL Query Validation
echo "Creating Issue #2: SQL Query Validation..."
gh issue create \
  --repo "$REPO" \
  --title "Implement SQL query safety validation to prevent injection vulnerabilities" \
  --label "security,enhancement,P0-critical" \
  --milestone "v0.2.0" \
  --body "## Problem
In \`infra/AnswerValidator.py\`, SQL queries are executed without safety validation. While queries are currently loaded from trusted files, there's no protection if user input is ever accepted in the future.

## Location
File: \`infra/AnswerValidator.py\`, line 85

\`\`\`python
def execute_query(self) -> None:
    # ...
    self.answer_df = pd.read_sql_query(self.query, conn, index_col=None)
\`\`\`

## Security Concern
- Potential SQL injection if user input is ever accepted
- No validation that queries don't contain malicious patterns
- Future feature additions could introduce vulnerabilities

## Proposed Solution

Add query validation before execution:

\`\`\`python
def _validate_query_safety(self, query: str) -> bool:
    \"\"\"
    Validate that query doesn't contain dangerous patterns.
    
    Args:
        query: SQL query string to validate
        
    Returns:
        True if query is safe
        
    Raises:
        SecurityError: If query contains forbidden operations
    \"\"\"
    # Only allow SELECT queries for practice platform
    forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 
                         'ALTER', 'CREATE', 'TRUNCATE', 'EXEC']
    
    query_upper = query.strip().upper()
    
    # Ensure query starts with SELECT or WITH (for CTEs)
    if not (query_upper.startswith('SELECT') or query_upper.startswith('WITH')):
        raise SecurityError(\"Only SELECT queries are allowed\")
    
    # Check for forbidden keywords
    for keyword in forbidden_keywords:
        if keyword in query_upper:
            raise SecurityError(f\"Query contains forbidden operation: {keyword}\")
    
    return True
\`\`\`

## Tasks
- [ ] Create SecurityError exception class
- [ ] Implement \`_validate_query_safety()\` method
- [ ] Call validation in \`execute_query()\` before execution
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
- OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"

echo "✓ Issue #2 created"
echo ""

# Issue 3: requirements-dev.txt
echo "Creating Issue #3: requirements-dev.txt..."
gh issue create \
  --repo "$REPO" \
  --title "Add requirements-dev.txt for development dependencies" \
  --label "enhancement,dependencies,P1-high,good first issue" \
  --milestone "v0.2.0" \
  --body "## Problem
No \`requirements-dev.txt\` file exists for development dependencies. Developers need to manually discover and install testing/linting tools.

## Impact
- Developers need to manually install testing/linting tools
- No standardized development environment
- CI/CD pipeline requirements not documented
- Inconsistent tooling across contributors

## Proposed Solution

Create \`requirements-dev.txt\`:

\`\`\`txt
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
\`\`\`

## Tasks
- [ ] Create \`requirements-dev.txt\` file
- [ ] Add testing dependencies (pytest, pytest-cov)
- [ ] Add linting dependencies (flake8, black, isort, pylint)
- [ ] Add type checking dependencies (mypy)
- [ ] Add documentation dependencies (sphinx)
- [ ] Add security scanning dependencies (bandit, safety)
- [ ] Update README.md with development setup instructions
- [ ] Update CONTRIBUTING.md (if exists) with tooling information

## Installation Command
After creation, developers can install with:
\`\`\`bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
\`\`\`

## References
- PROJECT_REVIEW.md Issue #3"

echo "✓ Issue #3 created"
echo ""

# Issue 4: CI/CD Pipeline
echo "Creating Issue #4: CI/CD Pipeline..."
gh issue create \
  --repo "$REPO" \
  --title "Add GitHub Actions workflow for CI/CD" \
  --label "infrastructure,ci/cd,P1-high" \
  --milestone "v0.2.0" \
  --body "## Problem
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

## Tasks
- [ ] Create \`.github/workflows/ci.yml\`
- [ ] Add lint job (flake8, black, isort, mypy)
- [ ] Add test job with matrix for Python 3.10, 3.11, 3.12
- [ ] Add security scan job (bandit, safety)
- [ ] Configure codecov for coverage reporting
- [ ] Add status badges to README.md
- [ ] Test workflow with a PR
- [ ] Document CI/CD process in CONTRIBUTING.md

## References
- PROJECT_REVIEW.md Issue #13
- PRODUCT_ROADMAP.md TASK-014"

echo "✓ Issue #4 created"
echo ""

# Issue 5: Test Coverage
echo "Creating Issue #5: Test Coverage..."
gh issue create \
  --repo "$REPO" \
  --title "Add comprehensive tests for AnswerValidator and logging_config" \
  --label "testing,P1-high,enhancement" \
  --milestone "v0.3.0" \
  --body "## Problem
Critical modules lack test coverage:
- \`infra/AnswerValidator.py\` - No tests found
- \`infra/logging_config.py\` - No tests found
- Integration tests missing for \`SQl_answer.py\`

## Current Coverage
Existing tests:
- ✅ \`test_data_generator.py\` - Basic tests
- ✅ \`test_difficulty.py\` - Difficulty system tests
- ✅ \`test_user_system.py\` - User management tests

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

## Tasks
- [ ] Create \`tests/test_answer_validator.py\`
- [ ] Create \`tests/test_logging_config.py\`
- [ ] Create \`tests/test_integration.py\` for end-to-end tests
- [ ] Add fixtures for test data and databases
- [ ] Aim for 80%+ code coverage
- [ ] Run coverage report: \`pytest --cov=infra --cov-report=html\`
- [ ] Document testing approach in README

## Coverage Goal
Target: 80%+ coverage for all modules in \`infra/\`

## References
- PROJECT_REVIEW.md Issue #12
- PRODUCT_ROADMAP.md TASK-010"

echo "✓ Issue #5 created"
echo ""

# Issue 6: Type Hints
echo "Creating Issue #6: Type Hints..."
gh issue create \
  --repo "$REPO" \
  --title "Add complete type hints to all public methods and functions" \
  --label "code-quality,P2-medium,enhancement" \
  --milestone "v0.3.0" \
  --body "## Problem
While some files have type hints (e.g., \`user.py\`, \`DataGenerator.py\`), many functions lack complete type annotations.

## Impact
- Reduced code readability
- Harder to catch type-related bugs
- Poor IDE autocomplete support
- Not following modern Python best practices (PEP 484)

## Tasks
- [ ] Add type hints to \`infra/logging_config.py\`
- [ ] Add type hints to \`SQl_answer.py\`
- [ ] Review and complete type hints in \`infra/AnswerValidator.py\`
- [ ] Review and complete type hints in \`infra/DataGenerator.py\`
- [ ] Add type hints to all test files
- [ ] Run mypy to validate type hints: \`mypy infra/ --strict\`
- [ ] Update any dynamically typed sections with proper annotations
- [ ] Document type hint conventions in CONTRIBUTING.md

## Type Hint Guidelines
- Use \`typing.Optional[T]\` for nullable types
- Use \`typing.Union[T1, T2]\` for multiple allowed types
- Use \`typing.List[T]\`, \`typing.Dict[K, V]\` for collections
- Use \`typing.Any\` sparingly, only when truly necessary
- Add return type annotations to all functions
- Use \`-> None\` for functions without return value

## References
- PROJECT_REVIEW.md Issue #4
- PEP 484: https://www.python.org/dev/peps/pep-0484/"

echo "✓ Issue #6 created"
echo ""

# Issue 7: Error Handling
echo "Creating Issue #7: Error Handling..."
gh issue create \
  --repo "$REPO" \
  --title "Add comprehensive error handling across all modules" \
  --label "code-quality,P2-medium,enhancement" \
  --milestone "v0.3.0" \
  --body "## Problem
Error handling is inconsistent across modules. Some methods have try-except blocks while others let exceptions propagate without context.

## Impact
- Unclear error messages for users
- Potential for unhandled exceptions
- Difficult debugging
- Poor user experience

## Tasks
- [ ] Add error handling to \`DataGenerator.load_yaml_config()\`
- [ ] Add error handling to \`DataGenerator.write_to_csv()\`
- [ ] Add error handling to \`DataGenerator.save_to_sqlite()\`
- [ ] Add error handling to file I/O operations in \`AnswerValidator\`
- [ ] Add error handling to \`LoggerManager\` initialization
- [ ] Create custom exception classes if needed
- [ ] Add error handling documentation
- [ ] Add tests for error conditions

## Error Handling Guidelines
1. Catch specific exceptions, not broad \`Exception\`
2. Provide context in error messages
3. Include suggestions for resolution
4. Log errors before re-raising
5. Document all raised exceptions in docstrings

## References
- PROJECT_REVIEW.md Issue #5"

echo "✓ Issue #7 created"
echo ""

# Issue 8: pyproject.toml
echo "Creating Issue #8: pyproject.toml..."
gh issue create \
  --repo "$REPO" \
  --title "Add pyproject.toml for PEP 517/518 compliance" \
  --label "infrastructure,P2-medium,enhancement" \
  --milestone "v0.3.0" \
  --body "## Problem
The project lacks a proper package configuration file, preventing:
- Installation as editable package (\`pip install -e .\`)
- Proper dependency management
- Following modern Python packaging standards

## Impact
- Cannot install project as package
- Import path issues
- Not following PEP 517/518 standards
- Harder to distribute

## Tasks
- [ ] Create \`pyproject.toml\` with above configuration
- [ ] Test installation: \`pip install -e .\`
- [ ] Test dev installation: \`pip install -e \".[dev]\"\`
- [ ] Update README.md installation instructions
- [ ] Update Dockerfile to use pyproject.toml
- [ ] Verify all tools (black, mypy, pytest) use config from pyproject.toml
- [ ] Remove redundant configuration files if any

## After Creation
Developers can install with:
\`\`\`bash
# Regular installation
pip install -e .

# Development installation with all tools
pip install -e \".[dev]\"
\`\`\`

## References
- PROJECT_REVIEW.md Issue #15
- PRODUCT_ROADMAP.md TASK-001"

echo "✓ Issue #8 created"
echo ""

# Issue 9: Input Validation
echo "Creating Issue #9: Input Validation..."
gh issue create \
  --repo "$REPO" \
  --title "Implement input validation in DataGenerator" \
  --label "security,code-quality,P2-medium" \
  --milestone "v0.3.0" \
  --body "## Problem
\`DataGenerator\` accepts user input without validation:
- \`num_records\` can be negative or extremely large
- \`seed\` can be any value
- YAML config structure not validated

## Impact
- Potential DoS through memory exhaustion
- Unexpected behavior with invalid inputs
- Poor error messages
- Security risk

## Tasks
- [ ] Add \`_validate_num_records()\` method
- [ ] Add \`_validate_config()\` method
- [ ] Add \`_validate_seed()\` method if needed
- [ ] Call validation methods in \`__init__()\`
- [ ] Add tests for validation methods
- [ ] Add tests for edge cases (negative, zero, very large)
- [ ] Update docstrings with validation information

## Validation Rules
- \`num_records\`: Must be 1 <= n <= 10,000,000
- \`seed\`: Must be non-negative integer if provided
- Config must have required keys: 'data_generation', 'fields'
- Each field must have: 'name', 'type', 'values'

## References
- PROJECT_REVIEW.md Issue #9"

echo "✓ Issue #9 created"
echo ""

# Issue 10: Docstrings
echo "Creating Issue #10: Docstrings..."
gh issue create \
  --repo "$REPO" \
  --title "Complete docstring coverage following PEP 257" \
  --label "documentation,code-quality,P2-medium,good first issue" \
  --milestone "v0.3.0" \
  --body "## Problem
Several functions and modules lack docstrings:
- \`infra/logging_config.py\` - Missing module and class docstrings
- \`SQl_answer.py\` - Missing function docstrings
- Various helper methods lack documentation

## Impact
- Harder for new contributors to understand code
- Poor IDE documentation support
- Not following PEP 257
- Difficult to generate API documentation

## Tasks
- [ ] Add module docstrings to all Python files
- [ ] Add class docstrings with Attributes section
- [ ] Add method docstrings with Args, Returns, Raises
- [ ] Add docstrings to \`infra/logging_config.py\`
- [ ] Add docstrings to \`SQl_answer.py\`
- [ ] Review existing docstrings for completeness
- [ ] Add examples in docstrings where helpful
- [ ] Run docstring linter: \`pydocstyle infra/\`
- [ ] Generate API docs with sphinx to verify

## References
- PROJECT_REVIEW.md Issue #10
- PEP 257: https://www.python.org/dev/peps/pep-0257/"

echo "✓ Issue #10 created"
echo ""

# Issue 11: README Fix
echo "Creating Issue #11: README Fix..."
gh issue create \
  --repo "$REPO" \
  --title "Update README.md Quick Start to reflect actual usage" \
  --label "documentation,P2-medium,good first issue" \
  --milestone "v0.2.0" \
  --body "## Problem
The README.md Quick Start guide shows commands that don't work:

\`\`\`bash
# From README
python SQl_answer.py sql_basic_select
\`\`\`

But \`SQl_answer.py\` doesn't accept command-line arguments in its current implementation.

## Impact
- New users cannot follow quick start guide
- Poor first-time user experience
- Misleading documentation
- Frustration for contributors

## Tasks
- [ ] Decide on updating README or adding CLI support
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
- PROJECT_REVIEW.md Issue #11"

echo "✓ Issue #11 created"
echo ""

# Issue 12: YAML Validation
echo "Creating Issue #12: YAML Validation..."
gh issue create \
  --repo "$REPO" \
  --title "Implement schema validation for YAML configuration files" \
  --label "enhancement,configuration,P2-medium" \
  --milestone "v0.4.0" \
  --body "## Problem
YAML configuration files (\`config.yml\`, \`questions_config.yml\`) are loaded but not validated against a schema. Invalid configurations cause runtime errors with poor error messages.

## Impact
- Invalid config causes runtime errors
- Poor error messages when config is wrong
- Hard to debug configuration issues
- No validation feedback for contributors

## Tasks
- [ ] Create \`infra/config/schemas.py\` with JSON schemas
- [ ] Add jsonschema to requirements.txt
- [ ] Update \`DataGenerator.load_yaml_config()\` to validate
- [ ] Update question loading to validate questions_config.yml
- [ ] Add unit tests for schema validation
- [ ] Add tests for invalid configurations
- [ ] Document configuration format in docs/
- [ ] Add example configurations with comments

## References
- PROJECT_REVIEW.md Issue #16"

echo "✓ Issue #12 created"
echo ""

# Issue 13: Remove Commented Code
echo "Creating Issue #13: Remove Commented Code..."
gh issue create \
  --repo "$REPO" \
  --title "Clean up commented code in SQl_answer.py" \
  --label "cleanup,P3-low,good first issue" \
  --milestone "v0.4.0" \
  --body "## Problem
Large blocks of commented-out code exist in \`SQl_answer.py\` (lines 77-95).

## Impact
- Code clutter
- Confusion about intended functionality
- Harder to maintain

## Tasks
- [ ] Remove commented code from lines 77-95
- [ ] Check if examples should be preserved
- [ ] If yes, create \`examples/basic_usage.py\`
- [ ] Update documentation to reference examples
- [ ] Verify code still works after removal

## References
- PROJECT_REVIEW.md Issue #6"

echo "✓ Issue #13 created"
echo ""

# Issue 14: Rename File
echo "Creating Issue #14: Rename File..."
gh issue create \
  --repo "$REPO" \
  --title "Rename SQl_answer.py to sql_answer.py for PEP 8 compliance" \
  --label "refactoring,P3-low,good first issue" \
  --milestone "v0.4.0" \
  --body "## Problem
File name \`SQl_answer.py\` uses inconsistent capitalization. Should follow PEP 8 convention of lowercase with underscores.

## Impact
- Not following PEP 8 naming conventions
- Minor confusion for contributors
- Inconsistent with other file names

## Tasks
- [ ] Rename \`SQl_answer.py\` to \`sql_answer.py\`
- [ ] Update all import statements (if any)
- [ ] Update README.md references
- [ ] Update Dockerfile COPY command (line 42)
- [ ] Update docker-compose.yml if referenced
- [ ] Update any documentation mentioning the file
- [ ] Test that everything still works

## Files to Update
- \`Dockerfile\` line 42
- \`README.md\` (multiple references)
- \`docker-compose.yml\` (check if referenced)
- Any other documentation

## Git Command
\`\`\`bash
git mv SQl_answer.py sql_answer.py
\`\`\`

## References
- PROJECT_REVIEW.md Issue #7"

echo "✓ Issue #14 created"
echo ""

# Issue 15: Documentation Fix
echo "Creating Issue #15: Documentation Fix..."
gh issue create \
  --repo "$REPO" \
  --title "Update README.md folder name reference (solutions vs Sloutions)" \
  --label "documentation,P3-low,good first issue" \
  --milestone "v0.4.0" \
  --body "## Problem
README.md line 104 mentions a typo in folder naming that doesn't appear to exist.

## Investigation Needed
1. Check if \"Sloutions\" folder exists anywhere in the project
2. Verify actual folder structure matches documentation
3. Remove incorrect comment if folder is correctly named

## Tasks
- [ ] Search for any folders named \"Sloutions\": \`find . -type d -name \"*lout*\"\`
- [ ] Verify \`Questions/*/solutions/\` all use correct spelling
- [ ] If all folders are correct, update README.md line 104
- [ ] If typo exists, create issue to fix folder names
- [ ] Remove reference to non-existent TASK-011

## References
- PROJECT_REVIEW.md Issue #14
- README.md line 104"

echo "✓ Issue #15 created"
echo ""

# Issue 16: Placeholder (count alignment)
echo "Creating Issue #16: Update Documentation Consistency..."
gh issue create \
  --repo "$REPO" \
  --title "Ensure documentation consistency across all files" \
  --label "documentation,P3-low" \
  --milestone "v0.4.0" \
  --body "## Problem
Minor inconsistencies exist across documentation files that should be harmonized.

## Tasks
- [ ] Review all markdown files for consistency
- [ ] Ensure issue counts match across documents
- [ ] Verify all cross-references are accurate
- [ ] Update any outdated information
- [ ] Standardize formatting and style

## References
- PROJECT_REVIEW.md
- ISSUES_TO_CREATE.md
- SUMMARY.md"

echo "✓ Issue #16 created"
echo ""

echo "========================================="
echo "All 16 issues created successfully!"
echo "========================================="
echo ""
echo "View issues at: https://github.com/$REPO/issues"
