# Git Setup Guide for Tile Swap

## Line Ending Issues

### Problem
Git on Windows may have issues with line endings, which can cause markdown files to not render properly on GitHub/GitLab.

### Solution
We've created a `.gitattributes` file that ensures all text files use Unix-style (LF) line endings.

## Files Created

### 1. `.gitattributes`
Tells Git how to handle line endings for different file types.

```
*.py text eol=lf
*.md text eol=lf
*.txt text eol=lf
```

### 2. `normalize_line_endings.py`
Script to convert all existing files to LF line endings.

## Git Configuration Commands

### Configure Git for This Repository

Run these commands in your repository:

```bash
# Configure Git to use LF for checkout and commit
git config core.autocrlf input

# Configure Git to warn about mixed line endings
git config core.safecrlf warn

# Re-normalize all files
git add --renormalize .
git status
```

### Global Git Configuration (Optional)

To apply these settings to all your Git repositories:

```bash
# Set autocrlf globally
git config --global core.autocrlf input

# Set safecrlf globally
git config --global core.safecrlf warn
```

## What These Settings Do

### `core.autocrlf = input`
- **On commit**: Converts CRLF → LF
- **On checkout**: Leaves as-is (keeps LF)
- **Best for**: Cross-platform projects, committing to GitHub

### `core.safecrlf = warn`
- Warns if a file has mixed line endings
- Helps catch line ending issues before they cause problems

## Fixing Existing Repository

If you already have files committed with CRLF line endings:

```bash
# 1. Ensure .gitattributes is in place
git add .gitattributes

# 2. Remove all files from Git's index
git rm --cached -r .

# 3. Re-add all files (Git will normalize based on .gitattributes)
git add .

# 4. Commit the normalized files
git commit -m "Normalize line endings to LF"
```

## Verifying Line Endings

### Check a Single File
```bash
file README.md
```

Should show: `README.md: ASCII text` (not `ASCII text, with CRLF line terminators`)

### Check All Python Files
```bash
file *.py
```

### Using Python Script
```bash
python normalize_line_endings.py
```

## Common Issues and Solutions

### Issue 1: Markdown Not Rendering on GitHub

**Cause:** Mixed or CRLF line endings

**Solution:**
```bash
python normalize_line_endings.py
git add --renormalize .
git commit -m "Fix line endings"
git push
```

### Issue 2: Git Shows Changes Even When Nothing Changed

**Cause:** Line ending differences

**Solution:**
```bash
git config core.autocrlf input
git add --renormalize .
git status
```

### Issue 3: Files Show as Changed After Checkout

**Cause:** Autocrlf converting files

**Solution:**
```bash
git config core.autocrlf input
git reset --hard
```

## File Status

All files in this project currently have correct LF line endings:
- ✓ 17 Python files (.py) - LF
- ✓ 7 Markdown files (.md) - LF
- ✓ 1 Text file (.txt) - LF

## Best Practices

### For This Project
1. Always use `core.autocrlf = input` on Windows
2. The `.gitattributes` file is committed to the repository
3. All team members will get consistent line endings

### For New Files
1. Create files with LF line endings
2. Most modern editors support this (VS Code, Sublime, Atom, etc.)
3. Configure your editor to use LF for new files

### Editor Configuration

**VS Code:**
```json
{
  "files.eol": "\n"
}
```

**Sublime Text:**
```json
{
  "default_line_ending": "unix"
}
```

**Notepad++:**
Edit → EOL Conversion → Unix (LF)

## Checking Your Git Configuration

```bash
# View current config
git config -l | grep autocrlf
git config -l | grep safecrlf

# View global config
git config --global -l | grep autocrlf
```

## Summary

✓ `.gitattributes` file ensures consistent line endings
✓ All files currently have LF line endings
✓ Configure Git with `core.autocrlf = input`
✓ Use `git add --renormalize .` to fix existing files
✓ Markdown should render correctly on GitHub/GitLab

## Recommended Git Workflow

```bash
# Initial setup (once)
git config core.autocrlf input
git config core.safecrlf warn

# When you notice line ending issues
python normalize_line_endings.py
git add --renormalize .
git commit -m "Normalize line endings"
git push
```

## Still Having Issues?

If markdown still doesn't render after following these steps, the issue might be:

1. **GitHub cache** - Wait a few minutes or force refresh
2. **Invalid markdown syntax** - Validate markdown syntax
3. **File encoding** - Ensure files are UTF-8 encoded
4. **Special characters** - Remove any special Unicode characters

Run this to check encoding:
```bash
file -i README.md
```

Should show: `README.md: text/plain; charset=utf-8`
