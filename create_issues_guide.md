# Guide to Creating GitHub Issues from Project Review

This guide helps you create GitHub issues for all items identified in `PROJECT_REVIEW_ISSUES.md`.

## Quick Reference

**Total Issues to Create:** 15  
**Issue Templates Available:**
- `.github/ISSUE_TEMPLATE/ai_agent_bugfix.md` - For bugs
- `.github/ISSUE_TEMPLATE/ai_agent_feature.md` - For enhancements

---

## Issue Creation Commands

### Critical Issues (Create First)

#### ISSUE-001: Invalid Dependencies in requirements.txt
```bash
gh issue create \
  --title "[AI-BUG] Fix invalid dependencies in requirements.txt" \
  --label "bug,critical,dependencies,ai-agent-task" \
  --body-file .github/issues/issue-001.md
```

#### ISSUE-002: Schema Mismatch Between Data Generator and Example Question
```bash
gh issue create \
  --title "[AI-BUG] Fix schema mismatch between data generator and example questions" \
  --label "bug,critical,data-generation,ai-agent-task" \
  --body-file .github/issues/issue-002.md
```

---

### High Priority Issues

#### ISSUE-003: Missing Version Pinning in Dependencies
```bash
gh issue create \
  --title "[AI-BUG] Add version pinning to dependencies" \
  --label "bug,high,dependencies,ai-agent-task" \
  --body-file .github/issues/issue-003.md
```

#### ISSUE-004: Inconsistent File Naming Convention
```bash
gh issue create \
  --title "[AI-BUG] Rename SQl_answer.py to sql_answer.py" \
  --label "bug,high,code-quality,ai-agent-task" \
  --body-file .github/issues/issue-004.md
```

#### ISSUE-005: Missing Type Hints Throughout Codebase
```bash
gh issue create \
  --title "[AI-TASK] Add comprehensive type hints to codebase" \
  --label "enhancement,high,code-quality,ai-agent-task" \
  --body-file .github/issues/issue-005.md
```

#### ISSUE-006: No Package Installation Setup
```bash
gh issue create \
  --title "[AI-TASK] Add setup.py or pyproject.toml for package installation" \
  --label "enhancement,high,build,ai-agent-task" \
  --body-file .github/issues/issue-006.md
```

#### ISSUE-007: Potential SQL Injection Vulnerability
```bash
gh issue create \
  --title "[AI-BUG][SECURITY] Add SQL query validation and security measures" \
  --label "bug,security,high,ai-agent-task" \
  --body-file .github/issues/issue-007.md
```

---

### Medium Priority Issues

#### ISSUE-008: Missing Error Handling in DataGenerator
```bash
gh issue create \
  --title "[AI-BUG] Add comprehensive error handling to DataGenerator" \
  --label "bug,medium,error-handling,ai-agent-task" \
  --body-file .github/issues/issue-008.md
```

#### ISSUE-009: Duplicate Logging Handlers
```bash
gh issue create \
  --title "[AI-BUG] Fix potential duplicate logging handlers" \
  --label "bug,medium,logging,ai-agent-task" \
  --body-file .github/issues/issue-009.md
```

#### ISSUE-010: Missing Comprehensive Test Suite
```bash
gh issue create \
  --title "[AI-TASK] Implement comprehensive test suite" \
  --label "enhancement,medium,testing,ai-agent-task" \
  --body-file .github/issues/issue-010.md
```

#### ISSUE-011: No CI/CD Pipeline
```bash
gh issue create \
  --title "[AI-TASK] Set up CI/CD pipeline with GitHub Actions" \
  --label "enhancement,medium,devops,ai-agent-task" \
  --body-file .github/issues/issue-011.md
```

#### ISSUE-012: Missing Docstrings in Several Modules
```bash
gh issue create \
  --title "[AI-TASK] Add comprehensive docstrings to all modules" \
  --label "enhancement,medium,documentation,ai-agent-task" \
  --body-file .github/issues/issue-012.md
```

#### ISSUE-013: Path Handling Inconsistencies
```bash
gh issue create \
  --title "[AI-BUG] Standardize path handling using pathlib.Path" \
  --label "bug,medium,code-quality,ai-agent-task" \
  --body-file .github/issues/issue-013.md
```

---

### Low Priority Issues

#### ISSUE-014: Missing Pre-commit Hooks Configuration
```bash
gh issue create \
  --title "[AI-TASK] Add pre-commit hooks configuration" \
  --label "enhancement,low,developer-tools,ai-agent-task" \
  --body-file .github/issues/issue-014.md
```

#### ISSUE-015: Questions Directory Has Unclear Structure
```bash
gh issue create \
  --title "[AI-TASK] Add documentation and templates for Questions directory" \
  --label "enhancement,low,documentation,ai-agent-task" \
  --body-file .github/issues/issue-015.md
```

---

## Batch Creation Script

Create a bash script to generate all issues at once:

```bash
#!/bin/bash

# create_all_issues.sh
# This script creates all GitHub issues from the project review

echo "Creating GitHub issues from project review..."

# Function to create an issue
create_issue() {
  local title="$1"
  local labels="$2"
  local body_file="$3"
  
  echo "Creating: $title"
  gh issue create \
    --title "$title" \
    --label "$labels" \
    --body-file "$body_file"
  
  sleep 2  # Rate limiting
}

# Critical Issues
create_issue \
  "[AI-BUG] Fix invalid dependencies in requirements.txt" \
  "bug,critical,dependencies,ai-agent-task" \
  ".github/issues/issue-001.md"

create_issue \
  "[AI-BUG] Fix schema mismatch between data generator and example questions" \
  "bug,critical,data-generation,ai-agent-task" \
  ".github/issues/issue-002.md"

# High Priority
create_issue \
  "[AI-BUG] Add version pinning to dependencies" \
  "bug,high,dependencies,ai-agent-task" \
  ".github/issues/issue-003.md"

create_issue \
  "[AI-BUG] Rename SQl_answer.py to sql_answer.py" \
  "bug,high,code-quality,ai-agent-task" \
  ".github/issues/issue-004.md"

create_issue \
  "[AI-TASK] Add comprehensive type hints to codebase" \
  "enhancement,high,code-quality,ai-agent-task" \
  ".github/issues/issue-005.md"

create_issue \
  "[AI-TASK] Add setup.py or pyproject.toml for package installation" \
  "enhancement,high,build,ai-agent-task" \
  ".github/issues/issue-006.md"

create_issue \
  "[AI-BUG][SECURITY] Add SQL query validation and security measures" \
  "bug,security,high,ai-agent-task" \
  ".github/issues/issue-007.md"

# Medium Priority
create_issue \
  "[AI-BUG] Add comprehensive error handling to DataGenerator" \
  "bug,medium,error-handling,ai-agent-task" \
  ".github/issues/issue-008.md"

create_issue \
  "[AI-BUG] Fix potential duplicate logging handlers" \
  "bug,medium,logging,ai-agent-task" \
  ".github/issues/issue-009.md"

create_issue \
  "[AI-TASK] Implement comprehensive test suite" \
  "enhancement,medium,testing,ai-agent-task" \
  ".github/issues/issue-010.md"

create_issue \
  "[AI-TASK] Set up CI/CD pipeline with GitHub Actions" \
  "enhancement,medium,devops,ai-agent-task" \
  ".github/issues/issue-011.md"

create_issue \
  "[AI-TASK] Add comprehensive docstrings to all modules" \
  "enhancement,medium,documentation,ai-agent-task" \
  ".github/issues/issue-012.md"

create_issue \
  "[AI-BUG] Standardize path handling using pathlib.Path" \
  "bug,medium,code-quality,ai-agent-task" \
  ".github/issues/issue-013.md"

# Low Priority
create_issue \
  "[AI-TASK] Add pre-commit hooks configuration" \
  "enhancement,low,developer-tools,ai-agent-task" \
  ".github/issues/issue-014.md"

create_issue \
  "[AI-TASK] Add documentation and templates for Questions directory" \
  "enhancement,low,documentation,ai-agent-task" \
  ".github/issues/issue-015.md"

echo "All issues created successfully!"
```

---

## Manual Creation via GitHub Web UI

If you prefer to create issues manually:

1. Go to https://github.com/moshesham/Practic_Questions_Platform/issues/new/choose
2. Select appropriate template (Bug Report or Feature Request)
3. Fill in details from `PROJECT_REVIEW_ISSUES.md`
4. Add labels as specified in the mapping table
5. Submit issue

---

## Issue Files Directory Structure

Create a `.github/issues/` directory with individual markdown files for each issue:

```
.github/
├── issues/
│   ├── issue-001.md  # requirements.txt fix
│   ├── issue-002.md  # schema mismatch
│   ├── issue-003.md  # version pinning
│   ├── ... (continues for all 15 issues)
```

Each file should contain the full issue description formatted according to the template.

---

## Next Steps After Creating Issues

1. **Organize into Milestones:**
   ```bash
   gh milestone create "Critical Fixes" --due-date 2025-12-14
   gh milestone create "High Priority" --due-date 2025-12-21
   gh milestone create "Medium Priority" --due-date 2026-01-15
   ```

2. **Assign to Milestones:**
   ```bash
   gh issue edit <issue-number> --milestone "Critical Fixes"
   ```

3. **Create Project Board:**
   - Go to Projects tab
   - Create new project: "Project Quality Improvements"
   - Add all created issues
   - Organize by priority

4. **Enable GitHub Actions:**
   - Review `.github/workflows/copilot-feature-factory.yml`
   - Enable automated issue assignment to AI agents

---

## Automation Tips

### Using GitHub CLI

Install if not already:
```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
```

Authenticate:
```bash
gh auth login
```

### Verify Created Issues

```bash
# List all issues with ai-agent-task label
gh issue list --label "ai-agent-task"

# List by priority
gh issue list --label "critical"
gh issue list --label "high"
gh issue list --label "medium"
```

---

## Template Reference

See:
- `PROJECT_REVIEW_ISSUES.md` - Full issue details
- `.github/ISSUE_TEMPLATE/ai_agent_bugfix.md` - Bug template
- `.github/ISSUE_TEMPLATE/ai_agent_feature.md` - Feature template

---

**Note:** This guide assumes you have GitHub CLI (`gh`) installed and authenticated. If not, issues can be created via the web interface.
