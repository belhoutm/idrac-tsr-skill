# Git Workflow Guide

This guide outlines the recommended Git workflow for the iDRAC-TSR-Skill project.

## Branching Strategy

### Main Branches

- **`master`**: Production-ready code. Always stable and deployable.
- **`develop`**: Integration branch for features (optional, for larger teams)

### Feature Branches

Create a new branch for each feature or bugfix:

```bash
git checkout -b feature/feature-name
# or
git checkout -b fix/issue-name
```

**Naming Conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions or updates

## Workflow Steps

### 1. Start New Work

```bash
# Ensure master is up to date
git checkout master
git pull origin master

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Small, Logical Changes

```bash
# Make your changes
# ... (edit files)

# Stage only the files for this specific change
git add specific-file.py
git add specific-file.md

# Commit with a clear, descriptive message
git commit -m "Add specific feature X"
```

**Commit Message Format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation change
- `style`: Code style change (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat: add error signature matching for NIC failures

Add pattern matching for NIC ASIC sensor failures in
signatures.yaml. This enables automatic detection of
hardware communication issues.

Closes #123
```

### 3. Test Your Changes

```bash
# Run any tests
# ... (run test commands)

# Verify functionality
# ... (manual testing)

# Check for issues
git status
git diff
```

### 4. Repeat for Each Logical Change

```bash
# Make next change
# ... (edit files)

# Stage and commit
git add next-file.py
git commit -m "Add next feature Y"

# Continue until feature is complete
```

### 5. Push Feature Branch

```bash
# Push your feature branch
git push -u origin feature/your-feature-name
```

### 6. Create Pull Request

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your feature branch
4. Compare to `master`
5. Add description of changes
6. Request review
7. Wait for approval

### 7. Merge After Approval

```bash
# Option 1: Merge via GitHub UI (recommended)
# Click "Merge Pull Request" on GitHub

# Option 2: Merge locally (if approved)
git checkout master
git pull origin master
git merge feature/your-feature-name
git push origin master

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## Git Aliases

Useful shortcuts configured in this project:

```bash
git co <branch>        # git checkout
git br                 # git branch
git ci                 # git commit
git st                 # git status
git unstage <file>     # git reset HEAD -- <file>
```

## Best Practices

### Commit Size

✅ **DO**: Small, focused commits
- One logical change per commit
- 50-200 lines changed ideally
- Clear, descriptive messages

❌ **DON'T**: Large, monolithic commits
- Multiple unrelated changes
- Hundreds of files changed
- Vague commit messages

### Commit Frequency

✅ **DO**: Commit often
- After each logical change
- After testing passes
- Before switching tasks

❌ **DON'T**: Commit rarely
- Only at end of day
- Only when "done"
- After making many changes

### Testing

✅ **DO**: Test before committing
- Run automated tests
- Manual verification
- Check for regressions

❌ **DON'T**: Commit untested code
- "I'll test later"
- "It probably works"
- Skip testing for speed

### Branch Management

✅ **DO**: Use feature branches
- One branch per feature
- Delete after merge
- Keep master clean

❌ **DON'T**: Commit directly to master
- Work on master
- Mix features on one branch
- Leave stale branches

## Example Workflow

### Adding a New Feature

```bash
# 1. Start from master
git checkout master
git pull origin master

# 2. Create feature branch
git checkout -b feature/add-nic-sensor-detection

# 3. Add error signature
vim skills/idrac/signatures.yaml
git add skills/idrac/signatures.yaml
git commit -m "feat: add NIC ASIC sensor failure signature"

# 4. Add test case
vim tests/test_nic_sensors.py
git add tests/test_nic_sensors.py
git commit -m "test: add NIC sensor detection tests"

# 5. Update documentation
vim skills/idrac/references.md
git add skills/idrac/references.md
git commit -m "docs: update NIC sensor documentation"

# 6. Push feature branch
git push -u origin feature/add-nic-sensor-detection

# 7. Create PR on GitHub
# ... (via GitHub UI)

# 8. Merge after approval
# ... (via GitHub UI or local merge)

# 9. Cleanup
git checkout master
git pull origin master
git branch -d feature/add-nic-sensor-detection
git push origin --delete feature/add-nic-sensor-detection
```

### Fixing a Bug

```bash
# 1. Start from master
git checkout master
git pull origin master

# 2. Create fix branch
git checkout -b fix/fix-password-change-logging

# 3. Make the fix
vim skills/idrac/scripts/tsr_analyzer.py
git add skills/idrac/scripts/tsr_analyzer.py
git commit -m "fix: correct password change event parsing"

# 4. Add regression test
vim tests/test_password_parsing.py
git add tests/test_password_parsing.py
git commit -m "test: add password parsing regression test"

# 5. Push and create PR
git push -u origin fix/fix-password-change-logging
# ... (create PR on GitHub)

# 6. Merge and cleanup
# ... (after approval)
```

## Troubleshooting

### Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
# Make corrections
git add .
git commit -m "corrected commit message"
```

### Undo Last Commit (Discard Changes)

```bash
git reset --hard HEAD~1
```

### Undo Unstaged Changes

```bash
git checkout -- file.py
```

### Undo Staged Changes

```bash
git unstage file.py
git checkout -- file.py
```

### Resolve Merge Conflicts

```bash
# When merging, if conflicts occur:
git status
# Edit conflicted files
# Resolve conflicts
git add resolved-file.py
git commit -m "resolve merge conflicts"
```

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
