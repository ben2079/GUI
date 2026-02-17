#!/bin/bash
# Install pre-commit hook to prevent accidental key leaks

HOOK_PATH=".git/hooks/pre-commit"

cat > "$HOOK_PATH" << 'EOF'
#!/bin/bash
# Pre-commit hook: Check for potential secrets

if git diff --cached --name-only | grep -E '(^|/)\.env(\.[a-zA-Z0-9_-]+)?$' >/dev/null 2>&1; then
    echo "❌ ERROR: Attempting to commit .env file!"
    echo "Remove it with: git reset HEAD <file>"
    exit 1
fi

if git diff --cached | grep -E 'sk-(proj-|svcacct-)?[a-zA-Z0-9_-]{20,}' >/dev/null 2>&1; then
    echo "❌ ERROR: Potential API key detected in staged changes!"
    echo "Review your changes before committing."
    exit 1
fi

exit 0
EOF

chmod +x "$HOOK_PATH"
echo "✅ Pre-commit hook installed at $HOOK_PATH"
