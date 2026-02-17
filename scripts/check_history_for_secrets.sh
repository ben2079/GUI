#!/bin/bash
# Check Git history for potential secrets
# This script scans the entire Git history for common secret patterns

set -e

echo "🔍 Scanning Git history for potential secrets..."
echo "This may take a moment for large repositories..."
echo ""

FOUND_ISSUES=0

# Check for OpenAI API keys
echo "Checking for OpenAI API keys (sk-*)..."
if git log -p | grep -n "sk-[A-Za-z0-9]\{20,\}" 2>/dev/null; then
    echo "⚠️  Found potential OpenAI API keys in Git history!"
    FOUND_ISSUES=1
fi

# Check for hardcoded personal paths
echo ""
echo "Checking for hardcoded personal paths (/home/ben, /home/benjamin)..."
if git log -p | grep -n -E "/home/(ben|benjamin)/" 2>/dev/null | head -20; then
    echo "⚠️  Found hardcoded personal paths in Git history!"
    FOUND_ISSUES=1
fi

# Check for environment variable assignments with potential secrets
echo ""
echo "Checking for API key assignments..."
if git log -p | grep -n -E "OPENAI_API_KEY\s*=\s*['\"]sk-" 2>/dev/null; then
    echo "⚠️  Found potential API key assignments in Git history!"
    FOUND_ISSUES=1
fi

# Check for .env files in history
echo ""
echo "Checking for committed .env files..."
if git log --all --full-history -- "**/.env" 2>/dev/null | head -20; then
    echo "⚠️  Found .env files in Git history!"
    FOUND_ISSUES=1
fi

echo ""
echo "================================"
if [ $FOUND_ISSUES -eq 0 ]; then
    echo "✅ No obvious secrets found in Git history"
    echo ""
    echo "Note: This is a basic check. For comprehensive scanning, consider:"
    echo "  - gitleaks: https://github.com/gitleaks/gitleaks"
    echo "  - trufflehog: https://github.com/trufflesecurity/trufflehog"
    exit 0
else
    echo "⚠️  POTENTIAL SECRETS FOUND IN GIT HISTORY!"
    echo ""
    echo "RECOMMENDED ACTIONS:"
    echo "1. Review the findings above carefully"
    echo "2. If real secrets were found:"
    echo "   a. Revoke any exposed API keys immediately"
    echo "   b. Use ./scripts/cleanup_git_history.sh to clean history"
    echo "   c. Force push the cleaned history"
    echo "3. For comprehensive scanning, use dedicated tools:"
    echo "   - gitleaks: https://github.com/gitleaks/gitleaks"
    echo "   - trufflehog: https://github.com/trufflesecurity/trufflehog"
    echo ""
    echo "See SECURITY.md for detailed instructions."
    exit 1
fi
