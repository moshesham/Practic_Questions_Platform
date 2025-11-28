# 🤖 Copilot Feature Factory

Automated prompt generation for **GitHub Copilot Pro** to streamline feature implementation using GitHub Actions.

## Overview

The Copilot Feature Factory is a GitHub Actions workflow that helps you implement features faster when using **GitHub Copilot Pro**. When you label an issue with `copilot-build`, it automatically generates an optimized prompt for Copilot Edits, Chat, or inline suggestions.

### How It Works (Copilot Pro Compatible)

This workflow is designed for **Copilot Pro users** who want to leverage AI assistance without needing Enterprise features:

1. **Label your issue** with `copilot-build`
2. **Workflow generates** a detailed, context-aware prompt
3. **Comment appears** on the issue with ready-to-use instructions
4. **You use** Copilot Edits/Chat with the provided prompt
5. **Copilot suggests** implementation based on your codebase
6. **You review** and accept the changes
7. **You create** the PR when ready

### Key Benefits

✅ **Works with Copilot Pro** - No Enterprise subscription needed  
✅ **Smart Prompts** - Automatically includes project context  
✅ **Flexible** - Use Copilot Edits, Chat, or inline suggestions  
✅ **Simple Setup** - Just add a label, get a prompt  
✅ **You Control** - Review and modify before committing  
✅ **No Cost** - Uses your existing Copilot subscription

## Setup

### Prerequisites

- GitHub Copilot subscription (**Pro**, Business, or Enterprise)
- VS Code with GitHub Copilot extension installed
- Repository with GitHub Actions enabled
- Local clone of your repository

### Installation

1. **The workflow file already exists** at:
   ```
   .github/workflows/copilot-feature-factory.yml
   ```

2. **Create the trigger label**:
   - Go to your repository on GitHub
   - Navigate to **Issues** → **Labels**
   - Click **New label**
   - Name: `copilot-build`
   - Color: `#7057ff` (or your preference)
   - Click **Create label**

3. **Optional: Create status label**:
   - Name: `copilot-ready`
   - Color: `#0E8A16`
   - This gets auto-added when prompt is ready

4. **Enable GitHub Actions** (if not already):
   - Go to **Settings** → **Actions** → **General**
   - Under "Actions permissions", select **Allow all actions and reusable workflows**
   - Click **Save**

That's it! No API keys, no enterprise features, no complex configuration.

## Usage

### Basic Workflow

1. **Create an Issue** with a clear, detailed description:
   ```markdown
   Title: Add user authentication feature
   
   Description:
   Implement a user authentication system:
   
   - Create login/logout functions
   - Use JWT tokens for session management
   - Add password hashing with bcrypt
   - Store credentials in existing database
   - Add validation for email format
   
   Files to modify/create:
   - src/auth.py (new file)
   - infra/user.py (add auth methods)
   
   Follow existing patterns in infra/ directory.
   ```

2. **Add the Label**: Apply `copilot-build` to trigger the workflow

3. **Get Your Prompt**: Within seconds, the workflow comments with:
   - ✨ Ready-to-use Copilot prompt with full context
   - 📖 Instructions for using Copilot Edits
   - 🛠️ Alternative approaches (Chat, inline)

4. **Use Copilot Edits**:
   - Open VS Code with your repo
   - Press `Ctrl+Shift+I` (or `Cmd+Shift+I` on Mac)
   - Paste the provided prompt
   - Review Copilot's multi-file suggestions
   - Accept/modify the changes

5. **Commit & Create PR**:
   - Commit the changes Copilot made
   - Push to a new branch
   - Create PR referencing the original issue
   - Merge when tests pass

### Writing Effective Issues

For best results, provide clear and detailed issue descriptions:

```markdown
## Feature Request: [Specific, Clear Title]

### What to Build
Clear description of what you want implemented.

### Technical Requirements
- Where the code should go (file paths)
- What libraries/frameworks to use
- How it should integrate with existing code
- Any specific patterns or conventions to follow

### Expected Behavior
- How should it work?
- What inputs and outputs?
- Edge cases to handle?

### Acceptance Criteria
- [ ] Specific testable requirement 1
- [ ] Specific testable requirement 2  
- [ ] Specific testable requirement 3

### Examples (Optional but Helpful)
- Code snippets showing desired usage
- Similar implementations in the codebase
- External references
```

**Tips for Better Results:**
- Be specific about file names and locations
- Mention existing code patterns to follow
- Include examples when possible
- List edge cases and error scenarios
- Reference related code or issues

## What Gets Created

When you label an issue with `copilot-build`, the workflow creates:

### In the Issue Comments

📝 **Structured Copilot Prompt** including:
- Issue title and requirements
- Technical guidelines (error handling, type hints, PEP 8)
- Project-specific context
- File structure information

📖 **Implementation Instructions** for:
- Using Copilot Edits (recommended)
- Using Copilot Chat with @workspace
- Using inline suggestions

🏷️ **Status Label**: `copilot-ready` added to issue

### What YOU Create (with Copilot's help)

✅ **Implementation code** - Generated via Copilot Edits/Chat  
✅ **Feature branch** - You create when ready  
✅ **Commits** - You commit the changes  
✅ **Pull Request** - You open when satisfied  

This gives you full control over the process while getting AI assistance!

## Workflow Details

### What the GitHub Action Does

**Trigger**: When you add the `copilot-build` label to any issue

**The workflow**:

1. **Extracts** issue title and description
2. **Formats** a comprehensive prompt including:
   - Your issue requirements
   - Project-specific context
   - Coding standards and guidelines
   - File structure information
3. **Posts** a comment to the issue with:
   - Ready-to-copy Copilot prompt
   - Step-by-step instructions
   - Multiple implementation options
4. **Adds** the `copilot-ready` label for tracking

**You then**:
- Copy the prompt from the issue comment
- Use it with Copilot Edits, Chat, or inline suggestions
- Review and refine the AI-generated code
- Commit and create your PR

### Why This Approach?

This workflow is designed for **GitHub Copilot Pro** users:

✅ **No Enterprise features required** - Works with individual Pro subscription  
✅ **You stay in control** - Review before committing  
✅ **Flexible** - Use any Copilot interface (Edits/Chat/Inline)  
✅ **Context-aware** - Includes your project patterns  
✅ **Optimized prompts** - Structured for best results  

## Customization

### Change the Trigger Label

Edit `.github/workflows/copilot-feature-factory.yml`:

```yaml
jobs:
  launch-copilot-agent:
    if: github.event.label.name == 'auto-implement'  # Change this
```

### Customize the Prompt

Modify what instructions Copilot receives:

```yaml
- name: 🤖 Launch GitHub Copilot Coding Agent
  uses: github/copilot-agent@v1
  with:
    task: |
      Your custom instructions here...
      
      Issue: #${{ github.event.issue.number }}
      ${{ github.event.issue.body }}
      
      Additional requirements:
      - Use TypeScript instead of JavaScript
      - Follow our specific style guide
      - Add comprehensive JSDoc comments
```

### Modify PR Template

Customize the pull request body:

```yaml
pr_body: |
  ## Your Custom PR Template
  
  Implemented by: GitHub Copilot
  Issue: Closes #${{ github.event.issue.number }}
  
  Your custom content here...
```

## Troubleshooting

### Common Issues

**1. Workflow doesn't trigger**
- ✅ Verify the label is exactly `copilot-build` (case-sensitive)
- ✅ Check that Actions are enabled (Settings → Actions)
- ✅ Ensure you have GitHub Copilot access
- ✅ Verify repository permissions

**2. "Copilot agent action not found" error**
- ✅ This requires GitHub Copilot Business or Enterprise
- ✅ Contact your organization admin to enable Copilot
- ✅ Check if your repo has Copilot enabled

**3. No PR created**
- ✅ Check Actions tab for error logs
- ✅ Issue description might be unclear - add more details
- ✅ Verify branch protection rules aren't blocking
- ✅ Check if there are permission issues

**4. Poor quality implementation**
- ✅ Make issue description more specific
- ✅ Reference existing code patterns
- ✅ Break complex requests into smaller issues
- ✅ Provide examples of desired output

**5. Copilot not understanding context**
- ✅ Mention specific files to modify
- ✅ Reference existing functions/classes
- ✅ Include code snippets as examples
- ✅ Link to related code or documentation

### Enable Debug Logging

Add these repository secrets for detailed logs:

```bash
ACTIONS_STEP_DEBUG = true
ACTIONS_RUNNER_DEBUG = true
```

Then check the Actions tab for verbose output.

## Limitations & Best Practices

### What Works Best

✅ **Well-scoped features** - Clear, specific requirements  
✅ **CRUD operations** - Create, read, update, delete functionality  
✅ **API endpoints** - REST API routes and handlers  
✅ **Data processing** - Transform, validate, parse data  
✅ **Utility functions** - Helper functions and modules  
✅ **Bug fixes** - Specific issues with clear reproduction steps  
✅ **Configuration changes** - Settings, configs, environment vars  

### What Might Need Human Review

⚠️ **Complex architecture** - Major structural changes  
⚠️ **Security-critical code** - Authentication, authorization, encryption  
⚠️ **Performance optimization** - May need profiling and testing  
⚠️ **Multi-service integration** - Requires deep system understanding  
⚠️ **Database migrations** - Review carefully before applying  

### Requirements

**GitHub Copilot Access**
- Requires GitHub Copilot Business or Enterprise subscription
- Individual Copilot accounts don't include coding agents
- Contact your GitHub organization admin if needed

**Repository Requirements**
- GitHub Actions must be enabled
- Repository must have Copilot enabled
- Sufficient Actions minutes in your plan

### Best Practices

1. **Start Small** - Test with simple issues first
2. **Be Specific** - Detailed descriptions get better results
3. **Review Everything** - Always review AI-generated code
4. **Test Thoroughly** - Run tests on generated code
5. **Provide Context** - Reference existing patterns and files
6. **Iterate** - If result isn't perfect, comment on PR for changes

## Security Considerations

### Code Review is Essential

🔒 **Always review AI-generated code** before merging:
- Check for security vulnerabilities
- Verify input validation
- Review error handling
- Test edge cases
- Validate dependencies

### Best Practices

1. **Never Auto-Merge** - Always have human review
2. **Test Thoroughly** - Run your test suite
3. **Check Dependencies** - Review any new packages added
4. **Security Scan** - Use tools like CodeQL, Dependabot
5. **Permissions** - Copilot uses standard GitHub permissions
6. **Data Privacy** - Copilot operates within GitHub's privacy policy

### What Copilot Can Access

✅ Your repository code (read-only during analysis)  
✅ Issue description and context  
✅ Public APIs and documentation  

❌ Your secrets or environment variables  
❌ Private data outside the repository  
❌ Other repositories without permission  ## Advanced Usage

### Multiple Labels for Different Behaviors

Create variants of the workflow:

```yaml
# .github/workflows/copilot-feature.yml
if: github.event.label.name == 'copilot-build'

# .github/workflows/copilot-bugfix.yml  
if: github.event.label.name == 'copilot-fix'
  with:
    task: |
      Fix the bug described in Issue #${{ github.event.issue.number }}
      Focus on minimal changes and thorough testing.
```

### Integration with Other Tools

Extend the workflow with additional steps:

```yaml
- name: 🔔 Notify Team
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "New PR created by Copilot: ${{ github.event.issue.title }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

- name: 🏷️ Auto-Label PR
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.addLabels({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.issue.number,
        labels: ['ai-generated', 'needs-review']
      });
```

### Custom Validation

Add checks after Copilot creates the PR:

```yaml
- name: 🧪 Run Tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov
    
- name: 🔍 Lint Code  
  run: |
    flake8 . --max-line-length=127
    black --check .
```

## Real-World Examples

### Example 1: Add New Feature

**Issue:**
```markdown
Title: Add CSV export for question data

Description:
Implement CSV export functionality for the practice questions.

Requirements:
- Create new function in `infra/DataGenerator.py`
- Function name: `export_to_csv(questions, filepath)`
- Include all question fields: id, text, difficulty, category
- Add proper error handling for file I/O
- Use pandas DataFrame for export
- Follow existing code style

Acceptance Criteria:
- [ ] Function exports DataFrame to CSV
- [ ] Handles missing/invalid filepath
- [ ] Preserves all question metadata
- [ ] Includes proper docstring
```

**Result:** Copilot creates PR with:
- Updated `infra/DataGenerator.py` with new export function
- Proper error handling
- Type hints and documentation
- Following existing patterns

### Example 2: Fix Bug

**Issue:**
```markdown
Title: Fix SQL injection vulnerability in query builder

Description:
The query builder in `SQl_answer.py` doesn't use parameterized queries.
This creates a security vulnerability.

Location: Line 45-60 in `SQl_answer.py`

Required changes:
- Replace string concatenation with parameterized queries
- Use SQLAlchemy's text() with bound parameters
- Validate all user inputs
- Add security comment

Example of vulnerable code:
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
```

Should be:
```python  
query = text("SELECT * FROM users WHERE id = :user_id")
result = conn.execute(query, {"user_id": user_id})
```

Acceptance Criteria:
- [ ] All queries use parameterization
- [ ] No string concatenation in SQL
- [ ] Input validation added
```

**Result:** Copilot creates PR with:
- Fixed SQL queries using parameterization
- Added input validation
- Security improvements
- Clear commit message explaining the fix

## Frequently Asked Questions

**Q: Do I need GitHub Copilot Enterprise?**  
A: No! This workflow is specifically designed for **GitHub Copilot Pro** (individual subscription). It also works with Business/Enterprise, but doesn't require those plans.

**Q: Does this automatically create PRs?**  
A: No. The workflow generates an optimized prompt and instructions. YOU use Copilot to implement and create the PR. This gives you full control.

**Q: What's the difference from enterprise coding agents?**  
A: Enterprise has autonomous agents that can create PRs automatically. With Pro, you use Copilot Edits/Chat with the prompts we generate, then you create the PR yourself.

**Q: Why not just use Copilot directly without the workflow?**  
A: The workflow creates structured, context-aware prompts that include your project patterns, file locations, and coding standards. This leads to much better suggestions.

**Q: Can I customize the prompt template?**  
A: Yes! Edit the workflow file (`.github/workflows/copilot-feature-factory.yml`) and modify the `copilotPrompt` section to match your needs.

**Q: Does this cost extra?**  
A: No! It uses your existing Copilot Pro subscription and free GitHub Actions minutes.

**Q: What if Copilot's suggestions aren't perfect?**  
A: Refine your issue description, add more context, or manually edit the suggested code. You're in full control of what gets committed.

**Q: Can I use this with other programming languages?**  
A: Absolutely! Just update the project context in the workflow to match your language/framework.

**Q: How do I disable this for certain issues?**  
A: Simply don't add the `copilot-build` label.

**Q: Can I use Copilot Chat instead of Edits?**  
A: Yes! The workflow comment includes instructions for multiple approaches including Chat with @workspace.

## Getting Help

### Resources

- 📖 [GitHub Copilot Documentation](https://docs.github.com/copilot)
- 📖 [GitHub Actions Documentation](https://docs.github.com/actions)  
- 💬 [GitHub Community Forum](https://github.community)
- 📧 Contact your GitHub organization admin for Copilot access

### Troubleshooting Steps

1. Check the [Actions tab](../../actions) for error logs
2. Verify GitHub Copilot is enabled for your organization
3. Ensure the issue description is clear and detailed
4. Review the [Troubleshooting](#troubleshooting) section above
5. Create an issue in this repository if you find bugs

---

**Happy Automating with GitHub Copilot! 🚀**
