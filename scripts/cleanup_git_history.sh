#!/bin/bash
# WARNING: This rewrites Git history. Use with caution.

echo "⚠️  This will rewrite Git history to remove sensitive data."
echo "   All collaborators will need to re-clone the repository."
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Install git-filter-repo if needed
if ! command -v git-filter-repo &> /dev/null; then
    echo "Installing git-filter-repo..."
    pip install git-filter-repo
fi

# Create backup
echo "Creating backup..."
git clone --mirror . ../ALDE-backup.git

# Remove patterns from history
echo "Removing sensitive patterns from history..."
git filter-repo --replace-text <(cat << 'EOF'
sk-(proj-|svcacct-)?[a-zA-Z0-9_-]{20,}==>API_KEY_REMOVED
/home/ben/==>/path/to/
/home/benjamin/==>/path/to/
OPENAI_API_KEY=sk-.*==>OPENAI_API_KEY=your_key_here
EOF
)

echo "✅ History cleaned. Backup saved to ../ALDE-backup.git"
echo ""
echo "Next steps:"
echo "1. Review changes with: git log --all --oneline"
echo "2. Force push: git push --force --all"
echo "3. Notify collaborators to re-clone"
