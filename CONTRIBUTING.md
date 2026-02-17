# Contributing to ALDE

Thank you for your interest in contributing to ALDE! This document provides guidelines for contributing to the project.

## 🔒 Security Guidelines

Before contributing, please review our security practices:

### Setup Your Development Environment

1. **Install the pre-commit hook** to prevent accidental secret commits:
   ```bash
   bash scripts/install-hooks.sh
   ```

2. **Configure your environment**:
   ```bash
   # Bootstrap local state
   python scripts/bootstrap_local_state.py
   
   # Copy and configure .env
   cp ALDE/ALDE/.env.example ALDE/ALDE/.env
   # Edit ALDE/ALDE/.env and add your API keys
   ```

### Security Best Practices

- **Never hardcode absolute paths** - use `Path(__file__).parent` for relative paths
- **Never commit API keys or secrets** - use environment variables
- **Use example data for testing** - not personal files or data
- **Review your changes** before committing:
  ```bash
  git diff --cached  # Review all staged changes
  git status         # Ensure no .env files are included
  ```

## 🧪 Testing Your Changes

### Run the Application

```bash
# Ensure your .env is configured
python scripts/bootstrap_local_state.py

# Run the application
python -m ALDE.ALDE.alde
```

### Run Tests (if available)

```bash
# Run tests from the repository root
pytest ALDE/ALDE/alde/Tests/
```

## 📝 Code Style

### Path Handling
- Use `pathlib.Path` for all file operations
- Use relative paths from `Path(__file__).parent`
- Never hardcode personal paths like `/home/username/`

Example:
```python
from pathlib import Path

# Good: Relative path
base_dir = Path(__file__).resolve().parent
data_file = base_dir / "data" / "example.json"

# Bad: Hardcoded absolute path
data_file = "/home/ben/data/example.json"
```

### Environment Variables
- Document all environment variables in `.env.example`
- Access environment variables using `os.getenv()` with sensible defaults
- Never hardcode secrets in source code

Example:
```python
import os
from pathlib import Path

# Good: Use environment variable with fallback
api_key = os.getenv("OPENAI_API_KEY")
app_data_dir = Path(os.getenv("AI_IDE_APPDATA_DIR", "AppData"))

# Bad: Hardcoded secret
api_key = "sk-1234567890abcdef"
```

### Import Style
- Use relative imports within the package
- Keep imports organized (standard library, third-party, local)

## 🔀 Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test your changes** thoroughly

4. **Commit with clear messages**:
   ```bash
   git add .
   git commit -m "Add feature: clear description of changes"
   ```

5. **Push to your fork** and create a pull request

6. **Respond to review feedback** promptly

## 🐛 Reporting Bugs

When reporting bugs, please include:

- A clear description of the issue
- Steps to reproduce the behavior
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant error messages or logs (with secrets redacted!)

## 💡 Suggesting Enhancements

We welcome suggestions for improvements! Please:

- Check existing issues to avoid duplicates
- Clearly describe the enhancement and its benefits
- Provide examples of how it would work
- Consider backward compatibility

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Publishing others' private information
- Trolling or insulting comments
- Other conduct inappropriate in a professional setting

## 📞 Getting Help

If you need help or have questions:

- Check existing documentation (README.md, QUICKSTART.md)
- Search through existing issues
- Open a new issue with the "question" label
- Be patient and respectful when asking for help

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!
