## Bug Reference

**Severity:** Critical  
**Component:** Build/Dependencies  
**Discovered:** December 7, 2025 - Code Review

---

## Current Behavior

The `requirements.txt` file includes Python standard library modules that cannot be installed via pip:

```
pandas
pyyaml
uuid
logging
```

When attempting to install dependencies:
```bash
pip install -r requirements.txt
```

Results in error:
```
ERROR: Could not find a version that satisfies the requirement uuid
ERROR: Could not find a version that satisfies the requirement logging
```

---

## Expected Behavior

The `requirements.txt` should only contain external packages that can be installed via pip. Standard library modules (`uuid`, `logging`) should not be listed.

---

## Steps to Reproduce

1. Clone the repository
2. Create a new virtual environment: `python -m venv venv`
3. Activate environment: `source venv/bin/activate`
4. Run: `pip install -r requirements.txt`
5. Observe installation failures

---

## Error Details

```
Collecting uuid
  ERROR: Could not find a version that satisfies the requirement uuid (from versions: none)
ERROR: No matching distribution found for uuid

Collecting logging
  ERROR: Could not find a version that satisfies the requirement logging (from versions: none)
ERROR: No matching distribution found for logging
```

---

## Affected Files

- `requirements.txt` - Lines 3-4 (uuid and logging)

---

## Root Cause Analysis

The `uuid` and `logging` modules are part of Python's standard library (available since Python 2.x). They are automatically available in any Python installation and should not be listed as external dependencies.

This appears to be a mistake where someone listed all imported modules without distinguishing between stdlib and third-party packages.

---

## Proposed Fix

Update `requirements.txt` to remove stdlib modules and add version constraints:

```
# Current (incorrect)
pandas
pyyaml
uuid
logging

# Fixed
pandas>=2.0.0,<3.0.0
pyyaml>=6.0,<7.0
```

**Changes:**
1. Remove `uuid` (stdlib)
2. Remove `logging` (stdlib)
3. Add version constraints to remaining packages
4. Add comments for clarity

**Recommended final version:**
```
# SQL Practice Questions Platform - Python Dependencies
# Python 3.10+ required

# Data manipulation
pandas>=2.0.0,<3.0.0

# Configuration parsing
pyyaml>=6.0,<7.0
```

---

## Acceptance Criteria

- [x] `uuid` removed from requirements.txt
- [x] `logging` removed from requirements.txt
- [x] Version constraints added to `pandas`
- [x] Version constraints added to `pyyaml`
- [x] `pip install -r requirements.txt` succeeds in clean environment
- [x] All existing functionality still works
- [x] No breaking changes to existing code

---

## AI Agent Instructions

1. **Update requirements.txt**
   - Remove `uuid` and `logging` lines
   - Add version constraints to remaining packages
   - Add comments for clarity

2. **Test the fix**
   - Create a new virtual environment
   - Install dependencies: `pip install -r requirements.txt`
   - Verify installation succeeds
   - Run existing code to ensure functionality

3. **Document the change**
   - Update any documentation that references dependencies
   - Add comment explaining version constraints

4. **Verify**
   - Ensure all imports still work
   - Run any existing tests
   - Check that data generation and validation still function

---

## Test Verification

```bash
# Create clean environment
python -m venv test_env
source test_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Should succeed without errors
echo "Installation successful if this prints"

# Test basic imports
python -c "import pandas; import yaml; import uuid; import logging; print('All imports successful')"

# Run data generation to verify functionality
python -m infra.DataGenerator

# Deactivate
deactivate
```

---

## Notes

- This is a blocking issue for new contributors/users
- Fix should be straightforward (< 5 minutes)
- No code changes required, only requirements.txt
- Consider creating `requirements-dev.txt` for development dependencies in the future
- After this fix, recommend creating ISSUE-003 for adding proper version constraints

---

## Related Issues

- See ISSUE-003 for comprehensive version pinning strategy
- See ISSUE-006 for proper package setup with pyproject.toml
