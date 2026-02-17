# Contributing to ALDE

Thank you for your interest in contributing to ALDE! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Initial Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ALDE.git
   cd ALDE
   ```

2. **Initialize submodules (if any):**
   ```bash
   git submodule update --init --recursive
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -e .
   ```

5. **Bootstrap local state:**
   ```bash
   python scripts/bootstrap_local_state.py
   ```

6. **Set up your API key:**
   ```bash
   # Copy the example environment file
   cp ALDE/ALDE/.env.example ALDE/ALDE/.env
   
   # Edit .env and add your API key:
   # OPENAI_API_KEY=sk-your-key-here
   ```

## 🔒 Security Requirements (MANDATORY)

Before submitting any contribution, you **MUST** follow these security guidelines:

### 1. Never Commit Secrets

❌ **NEVER commit:**
- API keys, tokens, or credentials
- `.env` files (already in `.gitignore`)
- Real personal data (CVs, cover letters, names, addresses)
- Files containing sensitive information

✅ **ALWAYS use:**
- Environment variables for secrets
- `.env` files for local configuration (ignored by Git)
- Placeholder data in examples ("Max Mustermann", not real names)
- Relative paths, never absolute paths with usernames

### 2. No Hardcoded Paths

❌ **BAD:**
```python
path = "/home/username/Projects/ALDE/data"
file = "/Users/jane/Documents/cv.pdf"
```

✅ **GOOD:**
```python
from pathlib import Path
path = Path(__file__).resolve().parent / "data"
file = Path(__file__).parent.parent / "AppData" / "cv.pdf"
```

### 3. Use the Bootstrap Script

Before submitting a PR, test that your changes work with a fresh setup:

```bash
# Clean your local state (optional, be careful!)
rm -rf ALDE/ALDE/AppData/*
rm ALDE/ALDE/.env ALDE/ALDE/db.json

# Re-bootstrap
python scripts/bootstrap_local_state.py

# Add your API key back
echo 'OPENAI_API_KEY=sk-...' > ALDE/ALDE/.env

# Test your changes
python -m ALDE.ALDE.alde
```

### 4. Check Before Committing

Run this before every commit:

```bash
# Check for secrets in staged changes
git diff --cached | grep -E "sk-[A-Za-z0-9]{20,}|OPENAI_API_KEY.*=.*sk-"

# If the above finds anything, DO NOT COMMIT
```

Better yet, install the pre-commit hook:

```bash
cp .githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## 📝 Contribution Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Use descriptive branch names:
- `feature/add-pdf-parser`
- `fix/api-key-loading`
- `docs/update-readme`
- `refactor/path-handling`

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style and patterns
- Add comments for complex logic
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run the application
python -m ALDE.ALDE.alde

# If there are tests, run them
pytest  # or whatever test runner is configured
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"
```

**Good commit messages:**
- `Add PDF extraction for job postings`
- `Fix API key loading from environment`
- `Update README with setup instructions`
- `Refactor path handling to use Path objects`

**Bad commit messages:**
- `Update`
- `Fix stuff`
- `WIP`
- `asdf`

### 5. Push and Create PR

```bash
git push origin your-branch-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what changed and why
- Reference any related issues
- Screenshots (if UI changes)
- Confirmation that security checks passed

## 🎨 Code Style

### Python Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings for public functions/classes
- Use type hints where appropriate

**Example:**
```python
from pathlib import Path
from typing import Optional

def load_config(config_path: Optional[Path] = None) -> dict:
    """
    Load configuration from file.
    
    Args:
        config_path: Path to config file. If None, uses default location.
        
    Returns:
        Configuration dictionary.
        
    Raises:
        FileNotFoundError: If config file doesn't exist.
    """
    if config_path is None:
        config_path = Path(__file__).parent / "config.json"
    
    with open(config_path) as f:
        return json.load(f)
```

### File Organization

- Keep related functionality together
- Use clear file and module names
- Don't create circular dependencies
- Follow the existing project structure

## 📦 Adding Dependencies

If you need to add a new dependency:

1. **Check if it's really needed:**
   - Can you use a standard library alternative?
   - Is there an existing dependency that can do this?

2. **Add to `pyproject.toml`:**
   ```toml
   [project]
   dependencies = [
       "existing-package>=1.0.0",
       "your-new-package>=2.3.0",
   ]
   ```

3. **Document why it's needed:**
   - Add a comment in `pyproject.toml`
   - Mention in your PR description

4. **Check for security issues:**
   - Review the package's security history
   - Check for known vulnerabilities
   - Prefer well-maintained packages

## 🐛 Reporting Bugs

### Before Reporting

- Check if the issue already exists
- Verify it's not a configuration problem
- Test with the latest version

### Bug Report Template

```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Ubuntu 22.04, macOS 13, Windows 11]
- Python version: [e.g., 3.11.5]
- ALDE version/commit: [e.g., commit abc123 or version 1.0.0]

**Additional Context:**
Any other relevant information, logs, screenshots, etc.
```

## 💡 Suggesting Features

Feature requests are welcome! Please include:

1. **Use case:** What problem does this solve?
2. **Proposed solution:** How should it work?
3. **Alternatives considered:** What other approaches did you think about?
4. **Additional context:** Mockups, examples, related features

## 📋 Pull Request Checklist

Before submitting your PR, verify:

- [ ] Code follows project style guidelines
- [ ] No API keys or secrets in code or commits
- [ ] No hardcoded personal paths (e.g., `/home/username/`)
- [ ] No real personal data in tracked files
- [ ] Used relative paths with `pathlib.Path`
- [ ] Tested with bootstrap script on clean state
- [ ] Added/updated documentation if needed
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains what and why
- [ ] All tests pass (if applicable)
- [ ] No merge conflicts with main branch

## 🔍 Code Review Process

1. **Automated checks:** CI will run automated tests
2. **Security review:** Changes will be checked for security issues
3. **Code review:** Maintainers will review your code
4. **Feedback:** Address any comments or requests
5. **Approval:** Once approved, your PR will be merged

## 🎯 Good First Issues

Looking for something to work on? Check issues labeled:
- `good first issue` - Great for newcomers
- `help wanted` - Community contributions welcome
- `documentation` - Improve docs
- `bug` - Fix existing issues

## 🤝 Community Guidelines

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Help others learn
- Give credit where due

## 📞 Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Security:** See SECURITY.md
- **Chat:** [Add your chat platform if available]

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

**Thank you for contributing to ALDE!** 🎉

Your contributions help make this project better for everyone.
