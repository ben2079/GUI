#!/bin/bash
# Helper script to clean Git history using git-filter-repo
# WARNING: This rewrites Git history - use with extreme caution!

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              GIT HISTORY CLEANUP SCRIPT                        ║"
echo "║                                                                ║"
echo "║  ⚠️  WARNING: This will rewrite Git history!                  ║"
echo "║                                                                ║"
echo "║  This is a DESTRUCTIVE operation that:                        ║"
echo "║  - Rewrites all commits in the repository                     ║"
echo "║  - Changes commit hashes                                      ║"
echo "║  - Requires force push to remote                              ║"
echo "║  - May cause issues for collaborators                         ║"
echo "║                                                                ║"
echo "║  Before proceeding:                                           ║"
echo "║  1. Backup your repository                                    ║"
echo "║  2. Coordinate with all collaborators                         ║"
echo "║  3. Revoke any exposed API keys first                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null; then
    echo "❌ Error: git-filter-repo is not installed"
    echo ""
    echo "Install it with:"
    echo "  pip install git-filter-repo"
    echo ""
    echo "Or see: https://github.com/newren/git-filter-repo"
    exit 1
fi

# Confirm user wants to proceed
read -p "Have you read and understood the warnings above? (type 'yes' to continue): " -r
echo
if [[ ! $REPLY == "yes" ]]; then
    echo "Aborted."
    exit 1
fi

read -p "Have you backed up your repository? (type 'yes' to continue): " -r
echo
if [[ ! $REPLY == "yes" ]]; then
    echo "Aborted. Please backup first."
    exit 1
fi

read -p "Have you coordinated with all collaborators? (type 'yes' to continue): " -r
echo
if [[ ! $REPLY == "yes" ]]; then
    echo "Aborted. Please coordinate with your team first."
    exit 1
fi

read -p "Have you revoked any exposed API keys? (type 'yes' to continue): " -r
echo
if [[ ! $REPLY == "yes" ]]; then
    echo "Aborted. Please revoke exposed keys at https://platform.openai.com/api-keys"
    exit 1
fi

echo ""
echo "Creating backup branch..."
git branch backup-before-cleanup 2>/dev/null || echo "Backup branch already exists"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "CLEANUP OPTIONS"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "What would you like to clean from history?"
echo ""
echo "1) Remove text patterns (API keys, hardcoded paths)"
echo "2) Remove specific files (.env, secrets.json, etc.)"
echo "3) Both text patterns and files"
echo "4) Custom (you provide git-filter-repo commands)"
echo "5) Cancel"
echo ""
read -p "Choose option (1-5): " -r OPTION
echo

case $OPTION in
    1)
        echo "Creating expressions file for text replacement..."
        cat > /tmp/git-filter-expressions.txt <<EOF
# Replace API keys with placeholder
regex:sk-[A-Za-z0-9]{20,}==>sk-REDACTED-KEY

# Replace hardcoded paths
regex:/home/ben/[^\s]*==>/path/to/project
regex:/home/benjamin/[^\s]*==>/path/to/project
EOF
        
        echo ""
        echo "This will replace:"
        echo "  - API keys (sk-...) with 'sk-REDACTED-KEY'"
        echo "  - /home/ben/* paths with '/path/to/project'"
        echo "  - /home/benjamin/* paths with '/path/to/project'"
        echo ""
        read -p "Proceed? (yes/no): " -r
        if [[ $REPLY == "yes" ]]; then
            git-filter-repo --replace-text /tmp/git-filter-expressions.txt --force
            echo "✅ Text patterns replaced in history"
        else
            echo "Aborted."
            exit 1
        fi
        ;;
        
    2)
        echo ""
        echo "Enter filenames to remove from history (one per line, empty line to finish):"
        echo "Example: ALDE/ALDE/.env"
        echo ""
        
        FILES_TO_REMOVE=()
        while IFS= read -r line; do
            [[ -z "$line" ]] && break
            FILES_TO_REMOVE+=("$line")
        done
        
        if [ ${#FILES_TO_REMOVE[@]} -eq 0 ]; then
            echo "No files specified. Aborted."
            exit 1
        fi
        
        echo ""
        echo "Will remove these files from history:"
        printf '  - %s\n' "${FILES_TO_REMOVE[@]}"
        echo ""
        read -p "Proceed? (yes/no): " -r
        
        if [[ $REPLY == "yes" ]]; then
            for file in "${FILES_TO_REMOVE[@]}"; do
                git-filter-repo --path "$file" --invert-paths --force
            done
            echo "✅ Files removed from history"
        else
            echo "Aborted."
            exit 1
        fi
        ;;
        
    3)
        echo "Combining text replacement and file removal..."
        
        # Text replacement first
        cat > /tmp/git-filter-expressions.txt <<EOF
regex:sk-[A-Za-z0-9]{20,}==>sk-REDACTED-KEY
regex:/home/ben/[^\s]*==>/path/to/project
regex:/home/benjamin/[^\s]*==>/path/to/project
EOF
        
        git-filter-repo --replace-text /tmp/git-filter-expressions.txt --force
        
        # Then remove common secret files
        echo ""
        echo "Removing common secret files (.env, etc.)..."
        git-filter-repo --path-glob '**/.env' --invert-paths --force
        
        echo "✅ History cleaned"
        ;;
        
    4)
        echo ""
        echo "Custom mode - you will run git-filter-repo commands manually."
        echo ""
        echo "Example commands:"
        echo "  # Replace text:"
        echo "  git-filter-repo --replace-text <(echo 'sk-old-key==>sk-REDACTED') --force"
        echo ""
        echo "  # Remove files:"
        echo "  git-filter-repo --path .env --invert-paths --force"
        echo ""
        echo "See: https://github.com/newren/git-filter-repo"
        exit 0
        ;;
        
    5)
        echo "Cancelled."
        exit 0
        ;;
        
    *)
        echo "Invalid option."
        exit 1
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "CLEANUP COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Verify the changes:"
echo "   git log --oneline"
echo "   ./scripts/check_history_for_secrets.sh"
echo ""
echo "2. If satisfied, force push to remote:"
echo "   git push origin --force --all"
echo "   git push origin --force --tags"
echo ""
echo "3. Notify all collaborators to:"
echo "   git fetch origin"
echo "   git reset --hard origin/main  # or their branch"
echo ""
echo "4. If something went wrong, restore from backup:"
echo "   git reset --hard backup-before-cleanup"
echo ""
echo "⚠️  Remember: Force pushing affects everyone!"
echo ""
