# GitHub Issues Directory

This directory contains pre-written issue descriptions ready to be posted to GitHub.

## Purpose

These issue markdown files were generated from a comprehensive code review conducted on December 7, 2025. Each file contains a complete issue description following the project's AI Agent task templates.

## Files Structure

```
.github/issues/
├── README.md           (this file)
├── issue-001.md       (Critical: Fix requirements.txt)
├── issue-002.md       (Critical: Fix schema mismatch)
└── [Additional issues to be created]
```

## How to Use These Files

### Option 1: Using GitHub CLI (Recommended)

```bash
# Create a single issue
gh issue create \
  --title "[AI-BUG] Fix invalid dependencies in requirements.txt" \
  --label "bug,critical,dependencies,ai-agent-task" \
  --body-file .github/issues/issue-001.md

# Or use the batch creation script from create_issues_guide.md
```

### Option 2: Manual Copy-Paste

1. Go to: https://github.com/moshesham/Practic_Questions_Platform/issues/new
2. Copy content from the appropriate issue-XXX.md file
3. Paste into the issue description
4. Add labels as specified in PROJECT_REVIEW_ISSUES.md
5. Submit

### Option 3: Automated Script

See `create_issues_guide.md` in the project root for batch creation scripts.

## Issue Mapping

| File | Title | Severity | Labels |
|------|-------|----------|--------|
| issue-001.md | Fix invalid dependencies in requirements.txt | Critical | bug, critical, dependencies |
| issue-002.md | Fix schema mismatch between data generator and examples | Critical | bug, critical, data-generation |
| issue-003.md | Add version pinning to dependencies | High | bug, high, dependencies |
| issue-004.md | Rename SQl_answer.py to sql_answer.py | High | bug, high, code-quality |
| issue-005.md | Add comprehensive type hints to codebase | High | enhancement, high, code-quality |
| issue-006.md | Add setup.py or pyproject.toml | High | enhancement, high, build |
| issue-007.md | Add SQL query validation (security) | High | bug, security, high |
| issue-008.md | Add error handling to DataGenerator | Medium | bug, medium, error-handling |
| issue-009.md | Fix duplicate logging handlers | Medium | bug, medium, logging |
| issue-010.md | Implement comprehensive test suite | Medium | enhancement, medium, testing |
| issue-011.md | Set up CI/CD pipeline | Medium | enhancement, medium, devops |
| issue-012.md | Add comprehensive docstrings | Medium | enhancement, medium, documentation |
| issue-013.md | Standardize path handling | Medium | bug, medium, code-quality |
| issue-014.md | Add pre-commit hooks | Low | enhancement, low, developer-tools |
| issue-015.md | Add Questions directory documentation | Low | enhancement, low, documentation |

## Status

- ✅ issue-001.md - Created
- ✅ issue-002.md - Created
- ⏳ issue-003.md through issue-015.md - To be created as needed

## Notes

- All issue templates follow the project's established AI Agent task format
- Each issue includes acceptance criteria, test verification steps, and AI agent instructions
- Issues are prioritized according to severity and impact
- Issues can be created individually or in batch using the provided scripts

## Related Documentation

- `../../PROJECT_REVIEW_ISSUES.md` - Complete review findings
- `../../create_issues_guide.md` - Detailed creation guide
- `../ISSUE_TEMPLATE/` - Original templates these are based on

---

**Last Updated:** December 7, 2025
