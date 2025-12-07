# How to Create GitHub Issues

This directory contains tools to help you create GitHub issues from the project review.

## Quick Start

### Option 1: Automated Script (Recommended)

Use the provided shell script to create all 16 issues automatically:

```bash
# Make sure you're authenticated with GitHub CLI
gh auth login

# Run the script
./create_issues.sh
```

This will create all 16 issues with proper:
- ✅ Titles
- ✅ Labels (bug, enhancement, P0-P3, etc.)
- ✅ Milestones (v0.2.0, v0.3.0, v0.4.0)
- ✅ Complete descriptions with code examples
- ✅ Task checklists

### Option 2: Manual Creation

If you prefer to create issues manually or selectively:

1. Open `ISSUES_TO_CREATE.md`
2. Find the issue you want to create
3. Copy the content (title, labels, description)
4. Go to https://github.com/moshesham/Practic_Questions_Platform/issues
5. Click "New Issue"
6. Paste the content and submit

### Option 3: GitHub CLI One-by-One

Create issues individually using the `gh` command:

```bash
# Example: Create Issue #1
gh issue create \
  --repo "moshesham/Practic_Questions_Platform" \
  --title "Fix requirements.txt - Remove stdlib modules and add version constraints" \
  --label "bug,dependencies,P0-critical,good first issue" \
  --milestone "v0.2.0" \
  --body-file <(sed -n '/^### Issue 1/,/^### Issue 2/p' ISSUES_TO_CREATE.md | tail -n +5 | head -n -3)
```

## Prerequisites

For automated creation, you need:
- GitHub CLI (`gh`) installed
- Authenticated with your GitHub account (`gh auth login`)
- Write access to the repository

### Install GitHub CLI

**macOS:**
```bash
brew install gh
```

**Ubuntu/Debian:**
```bash
sudo apt install gh
```

**Windows:**
```bash
winget install GitHub.cli
```

**Or download from:** https://cli.github.com/

## What Issues Will Be Created?

The script creates **16 issues** organized by priority:

### Critical (P0) - 2 issues
1. Fix requirements.txt - Remove stdlib modules and add version constraints
2. Implement SQL query safety validation to prevent injection vulnerabilities

### High (P1) - 4 issues
3. Add requirements-dev.txt for development dependencies
4. Add GitHub Actions workflow for CI/CD
5. Add comprehensive tests for AnswerValidator and logging_config
6. (Related infrastructure)

### Medium (P2) - 7 issues
7. Add complete type hints to all public methods and functions
8. Add comprehensive error handling across all modules
9. Add pyproject.toml for PEP 517/518 compliance
10. Implement input validation in DataGenerator
11. Complete docstring coverage following PEP 257
12. Update README.md Quick Start to reflect actual usage
13. Implement schema validation for YAML configuration files

### Low (P3) - 3 issues
14. Clean up commented code in SQl_answer.py
15. Rename SQl_answer.py to sql_answer.py for PEP 8 compliance
16. Update README.md folder name reference
17. Ensure documentation consistency

## Troubleshooting

### "gh: command not found"
Install the GitHub CLI (see prerequisites above).

### "authentication required"
Run `gh auth login` and follow the prompts.

### "permission denied: ./create_issues.sh"
Make the script executable: `chmod +x create_issues.sh`

### Issues already exist
The script will fail if issues with the same title already exist. You can either:
- Skip creating that issue
- Rename the existing issue
- Modify the script to update existing issues instead

## Customization

To modify which issues are created:
1. Edit `create_issues.sh`
2. Comment out sections for issues you don't want to create
3. Run the modified script

To change labels or milestones:
1. Edit the `--label` or `--milestone` parameters in `create_issues.sh`
2. Run the script

## After Creating Issues

Once issues are created:
1. Review them at https://github.com/moshesham/Practic_Questions_Platform/issues
2. Assign them to team members as appropriate
3. Add any additional labels or project boards
4. Start working on P0 (Critical) issues first

## Need Help?

- See `PROJECT_REVIEW.md` for detailed technical analysis
- See `ISSUES_TO_CREATE.md` for the full issue templates
- See `SUMMARY.md` for a quick start guide
