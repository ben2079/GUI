# Security Policy

## 🔒 Protecting Your API Keys

This project requires OpenAI API keys. **NEVER commit these to Git.**

### Setup
1. Copy `.env.example` to `.env`
2. Add your API key: `OPENAI_API_KEY=sk-...`
3. The `.env` file is already in `.gitignore`

### Before Pushing
- Run `git status` - ensure no `.env` files are staged
- Check for accidentally pasted keys in code comments
- Use the provided pre-commit hook (see Contributing)

## 📋 Reporting Vulnerabilities

If you discover a security issue, please email the repository maintainer instead of opening a public issue.

## 🛡️ Security Best Practices

### For Contributors
- Never hardcode absolute paths - use relative paths with `Path(__file__).parent`
- Never commit personal data or file paths
- Use environment variables for all sensitive configuration
- Test with example data, not personal files
- Install the pre-commit hook: `bash scripts/install-hooks.sh`

### For Users
- Keep your `.env` file private and never share it
- Rotate API keys immediately if you suspect they've been exposed
- Review your commit history before pushing to ensure no secrets are included
- Use the provided cleanup script if you accidentally commit sensitive data

## 🔍 What to Check Before Committing

Run these checks before every commit:

```bash
# Check for .env files
git status | grep -i "\.env"

# Check for potential API keys in staged changes
git diff --cached | grep -E "sk-[a-zA-Z0-9]{20,}"

# Check for hardcoded personal paths
git diff --cached | grep -E "/home/(ben|benjamin)/"
```

## 🚨 If You Accidentally Commit Secrets

1. **Immediately rotate the exposed API key** - get a new one from your provider
2. Remove the secret from Git history using the provided script: `bash scripts/cleanup_git_history.sh`
3. Force push the cleaned history (coordinate with collaborators first)
4. Never reuse the exposed key

## 📚 Additional Resources

- [GitHub: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OWASP: Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Git Filter-Repo Documentation](https://github.com/newren/git-filter-repo)
