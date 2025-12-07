# .gitignore Maintenance Guide

## Overview

This document explains the `.gitignore` structure and how to maintain it for the SQL Practice Questions Platform.

## Structure

The `.gitignore` is organized into logical sections:

1. **Python** - Python-specific artifacts
2. **IDEs and Editors** - Configuration files for various IDEs
3. **Operating Systems** - OS-specific files
4. **Project Specific** - SQL Practice Platform files
5. **Development & Testing** - Test outputs and profiling
6. **CI/CD & Deployment** - Docker, Kubernetes, Terraform
7. **Documentation** - Build outputs
8. **Backup & Temporary** - Temporary and backup files
9. **Security & Secrets** - Credentials and keys

## Key Patterns

### Always Ignored

```
__pycache__/          # Python bytecode cache
*.pyc, *.pyo         # Compiled Python files
.env                 # Environment variables with secrets
*.log                # Log files
output/*.db          # Generated databases
users/               # User progress data
logs/                # Log directory
```

### Exceptions (Not Ignored)

```
!.gitkeep            # Keep directory structure
!.env.example        # Example configuration
!config/*.example    # Example config files
Questions/*/solutions/*.csv  # Expected solution files
```

## Common Scenarios

### Adding a New Generated File Type

If you add a new type of generated file (e.g., `.parquet` files):

```bash
# Edit .gitignore
echo "*.parquet" >> .gitignore
echo "output/*.parquet" >> .gitignore

# Remove from tracking if already tracked
git rm --cached output/*.parquet

# Commit
git add .gitignore
git commit -m "chore: Ignore .parquet files"
```

### Preserving Empty Directories

To keep an empty directory in git:

```bash
# Create .gitkeep file
touch path/to/directory/.gitkeep

# Update .gitignore to allow .gitkeep
echo "!path/to/directory/.gitkeep" >> .gitignore

# Add with force flag
git add -f path/to/directory/.gitkeep
```

### Testing .gitignore Patterns

```bash
# Check if a file would be ignored
git check-ignore -v path/to/file

# List all ignored files
git status --ignored

# Test pattern before adding
git ls-files --others --ignored --exclude-from=.gitignore
```

## Best Practices

### ✅ DO:

- Keep sections organized and commented
- Test patterns before committing
- Document project-specific patterns
- Use `.env.example` for env var documentation
- Remove sensitive files immediately if accidentally committed

### ❌ DON'T:

- Ignore files needed for build/test
- Commit IDE-specific settings (unless team standard)
- Commit generated data that can be regenerated
- Commit credentials or API keys
- Over-ignore (be specific)

## Emergency: Removing Sensitive Data

If you accidentally commit sensitive data:

```bash
# Remove from latest commit
git rm --cached path/to/sensitive/file
git commit --amend

# Remove from history (use with caution)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner (recommended)
bfg --delete-files sensitive_file.txt
```

## File-Specific Notes

### User Progress Files (`users/`)

- Contains personal learning data
- Should NEVER be committed
- Backed up separately if needed
- Use `users/.gitkeep` to preserve directory

### Generated Data (`output/`)

- Database and CSV files
- Can be regenerated with:
  ```bash
  python infra/DataGenerator.py
  python infra/SchemaGenerator.py
  ```
- Only `output/.gitkeep` is tracked

### Logs (`logs/`)

- Application logs
- Can grow large
- Rotate logs regularly
- Only `logs/.gitkeep` is tracked

### AI Models (`models/`)

- Large binary files
- Use Git LFS if needed to track
- Consider cloud storage instead

## Verification Commands

```bash
# See what's currently ignored
git status --ignored

# Check a specific file
git check-ignore -v file.txt

# List all tracked files
git ls-files

# Find large files that shouldn't be tracked
git ls-files | xargs du -h | sort -h | tail -20

# Clean untracked files (DRY RUN first!)
git clean -ndX  # Show what would be removed
git clean -fdX  # Actually remove
```

## Integration with CI/CD

The `.gitignore` ensures:

- Clean repository without build artifacts
- No secrets in version control
- Reproducible builds (no local dependencies)
- Faster clone/pull operations

## Related Files

- `.env.example` - Environment variable template
- `.dockerignore` - Docker build exclusions
- `.gitattributes` - Git file handling rules

## Updates

When updating `.gitignore`:

1. Test patterns locally
2. Update this documentation if needed
3. Commit with clear message: `chore: Update .gitignore for X`
4. Announce to team if major changes

## Questions?

If unsure about a pattern, ask:

1. Will this file change on different machines? → Ignore
2. Is this generated or can be rebuilt? → Ignore
3. Does this contain secrets/credentials? → Ignore
4. Is this needed for builds on other machines? → Don't ignore

---

**Last Updated:** December 7, 2025
**Maintainer:** Development Team
