# Quick Start: Copilot Feature Factory

## 1-Minute Setup for GitHub Copilot Pro

### Step 1: Create the Label

1. Go to your repo's **Issues** tab
2. Click **Labels**
3. Click **New label**
4. Name: `copilot-build`
5. Color: Pick any color (suggest: purple `#7057ff`)
6. Click **Create label**

### Step 2: Create an Issue

```markdown
Title: Add hello world function

Description:
Create a simple function that returns "Hello, World!"

- Save it in: src/hello.py
- Add a docstring explaining the function
- Include type hints
- Follow PEP 8 style
```

### Step 3: Label It

Add the `copilot-build` label to your issue.

### Step 4: Get Your Prompt

The workflow will automatically comment on your issue with:
- ✅ A ready-to-use Copilot prompt
- ✅ Instructions for using Copilot Edits
- ✅ Alternative implementation approaches

### Step 5: Use Copilot Edits

1. **Open VS Code** with your repository
2. **Start Copilot Edits**: 
   - Press `Ctrl+Shift+I` (Windows/Linux)
   - Or `Cmd+Shift+I` (Mac)
   - Or click the sparkle icon ✨ in the sidebar
3. **Copy the prompt** from the issue comment
4. **Paste it** into Copilot Edits
5. **Review** the suggested changes
6. **Accept** what looks good
7. **Commit & Push**
8. **Create a Pull Request**

## What You Get

✅ **Structured Prompt** - Optimized for Copilot with all context  
✅ **Multiple Options** - Copilot Edits, Chat, or inline suggestions  
✅ **Context Aware** - Includes your project structure and patterns  
✅ **Ready to Use** - Just copy, paste, and review  

## Requirements

- ✅ GitHub Copilot Pro (or Business/Enterprise)
- ✅ VS Code with GitHub Copilot extension
- ✅ Repository cloned locally

**No enterprise features needed!** Works perfectly with Copilot Pro.

## Next Steps

- Try implementing a real feature from your backlog
- Customize the prompt template in the workflow
- Read the [full documentation](./COPILOT_FEATURE_FACTORY.md)

## Troubleshooting

**Workflow doesn't comment?**
- Check Actions are enabled in Settings
- Verify the label name is exactly `copilot-build`

**Copilot suggestions not helpful?**
- Make your issue description more detailed
- Include specific file paths and requirements
- Provide examples of similar existing code
