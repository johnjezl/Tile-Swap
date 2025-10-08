#!/bin/bash
# Fix Git markdown rendering issues
# Run this script to normalize line endings and configure Git properly

echo "========================================"
echo "Fixing Git Markdown Issues"
echo "========================================"
echo ""

echo "Step 1: Normalizing line endings..."
python normalize_line_endings.py
echo ""

echo "Step 2: Configuring Git for this repository..."
git config core.autocrlf input
git config core.safecrlf warn
echo "Git configured successfully!"
echo ""

echo "Step 3: Re-normalizing files in Git index..."
git add --renormalize .
echo ""

echo "Step 4: Checking status..."
git status
echo ""

echo "========================================"
echo "Fix complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Review the changes with: git diff --cached"
echo "2. Commit the changes with: git commit -m 'Fix line endings for markdown'"
echo "3. Push to remote with: git push"
echo ""
