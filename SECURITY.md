# Security Policy

## Overview

This project handles sensitive data including API keys, personal information, and documents. Following security best practices is essential to protect your data and credentials.

## 🔐 Protecting API Keys

### Never Commit API Keys

**Critical Rules:**
- ❌ Never commit `.env` files to version control
- ❌ Never hardcode API keys in source code
- ❌ Never commit files containing API keys or tokens
- ✅ Always use environment variables or `.env` files for secrets
- ✅ Keep `.env` in `.gitignore` (already configured)

### Setting Up API Keys

1. **Copy the example file:**
   ```bash
   cp ALDE/ALDE/.env.example ALDE/ALDE/.env
   ```

2. **Add your OpenAI API key to `ALDE/ALDE/.env`:**
   ```bash
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. **Verify the file is ignored:**
   ```bash
   git check-ignore ALDE/ALDE/.env
   # Should output: ALDE/ALDE/.env
   ```

### API Key Format

OpenAI API keys follow this pattern:
- Start with `sk-`
- Followed by 40-50 alphanumeric characters
- Example: `sk-proj-abcdefghijklmnopqrstuvwxyz1234567890ABCD`

**If you accidentally commit an API key:**
1. Revoke it immediately at https://platform.openai.com/api-keys
2. Generate a new key
3. Update your local `.env` file
4. Clean Git history (see "Git History Cleanup" section)

## 🛡️ Protecting Personal Data

### Personal Information

- Never commit real CVs, resumes, or cover letters to the repository
- Use the `AppData/` directory for personal documents (already ignored)
- Example templates use placeholder data ("Max Mustermann" = German "John Doe")
- Keep job postings and application materials in ignored directories

### Recommended Directory Structure

```
ALDE/ALDE/
├── AppData/               # ✅ Ignored - store personal files here
│   ├── VSM_4_Data/       # Job postings, CVs
│   ├── Cover_letters/    # Generated letters
│   └── generated/        # Other outputs
├── json_templates/       # ⚠️ Tracked - EXAMPLES ONLY
└── .env                  # ✅ Ignored - API keys here
```

## 🔍 Git History Cleanup

If you've accidentally committed secrets, use the provided tools:

### 1. Check for Secrets in History

```bash
./scripts/check_history_for_secrets.sh
```

This script scans your Git history for:
- API keys (patterns like `sk-...`)
- Hardcoded paths revealing usernames
- Environment variable assignments with secrets

### 2. Clean Git History (if needed)

⚠️ **WARNING: This rewrites Git history. Coordinate with all collaborators first.**

```bash
# Install git-filter-repo
pip install git-filter-repo

# Run the cleanup script
./scripts/cleanup_git_history.sh
```

### 3. Prevent Future Accidents

Install the pre-commit hook:

```bash
cp .githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

This hook will automatically check for secrets before each commit and block commits containing:
- OpenAI API keys
- Common secret patterns
- Hardcoded personal paths

## 📋 Security Checklist

Before contributing or deploying:

- [ ] API keys are in `.env` file, not in code
- [ ] `.env` file is in `.gitignore`
- [ ] No real personal data in tracked files
- [ ] No hardcoded absolute paths with usernames
- [ ] Pre-commit hook installed (optional but recommended)
- [ ] Scanned Git history for accidents (if contributing)

## 🚨 Reporting Vulnerabilities

If you discover a security vulnerability in this project:

### For Public Issues
- Open a GitHub Issue with the `security` label
- Describe the vulnerability clearly
- Include steps to reproduce (if applicable)
- Suggest a fix (if you have one)

### For Sensitive Issues
- **Do NOT** open a public issue
- Email the repository owner directly (find contact in GitHub profile)
- Allow reasonable time for a fix before public disclosure

### What to Report

Examples of security concerns:
- Exposed credentials in code or Git history
- Insecure API key handling
- Data leakage vulnerabilities
- Injection vulnerabilities
- Insecure dependencies

## 🔄 Regular Security Maintenance

### Monthly Tasks
- [ ] Review access logs (if using hosted services)
- [ ] Rotate API keys
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`
- [ ] Check for known vulnerabilities: `pip-audit`

### Before Each Release
- [ ] Run security scan: `./scripts/check_history_for_secrets.sh`
- [ ] Review all changes for accidental secrets
- [ ] Update dependencies
- [ ] Test with fresh `.env` configuration

## 📚 Additional Resources

- [OpenAI API Key Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Git Filter-Repo Documentation](https://github.com/newren/git-filter-repo)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

## 🆘 Emergency Response

**If you've exposed an API key publicly:**

1. **Immediately revoke the key:**
   - Go to https://platform.openai.com/api-keys
   - Find the exposed key
   - Click "Revoke"

2. **Generate a new key:**
   - Click "Create new secret key"
   - Save it securely in your `.env` file
   - Test that your application still works

3. **Clean the exposure:**
   - If in Git history: Use `cleanup_git_history.sh`
   - If in GitHub: Force push after cleanup
   - If in logs/screenshots: Delete or redact

4. **Monitor for abuse:**
   - Check your OpenAI usage dashboard
   - Look for unexpected API calls
   - Set up usage alerts if available

5. **Report the incident:**
   - Document what happened
   - Share lessons learned with the team
   - Update processes to prevent recurrence

---

**Last Updated:** 2026-02-17  
**Version:** 1.0
