#!/bin/bash
# Git Helper Script for iDRAC-TSR-Skill Project
# Provides shortcuts for common Git operations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show help
show_help() {
    cat << EOF
Git Helper Script - iDRAC-TSR-Skill

Usage: ./scripts/git-helpers.sh <command> [options]

Commands:
  new-feature <name>    Create a new feature branch
  new-fix <name>        Create a new fix branch
  save <message>        Stage all changes and commit
  push-feature          Push current branch to origin
  merge-feature         Merge current branch to master
  cleanup               Delete merged branches
  status                Show git status with branch info
  undo-last             Undo last commit (keep changes)
  undo-hard             Undo last commit (discard changes)

Examples:
  ./scripts/git-helpers.sh new-feature add-nic-sensor
  ./scripts/git-helpers.sh save "Add NIC sensor detection"
  ./scripts/git-helpers.sh push-feature
  ./scripts/git-helpers.sh merge-feature

EOF
}

# Create new feature branch
new_feature() {
    local branch_name="feature/$1"
    print_info "Creating feature branch: $branch_name"

    # Ensure master is up to date
    git checkout master
    git pull origin master

    # Create and checkout new branch
    git checkout -b "$branch_name"
    print_success "Created and checked out branch: $branch_name"
}

# Create new fix branch
new_fix() {
    local branch_name="fix/$1"
    print_info "Creating fix branch: $branch_name"

    # Ensure master is up to date
    git checkout master
    git pull origin master

    # Create and checkout new branch
    git checkout -b "$branch_name"
    print_success "Created and checked out branch: $branch_name"
}

# Stage all changes and commit
save() {
    local message="$1"
    if [ -z "$message" ]; then
        print_error "Please provide a commit message"
        exit 1
    fi

    print_info "Staging all changes..."
    git add -A

    print_info "Committing with message: $message"
    git commit -m "$message"
    print_success "Changes committed"
}

# Push current branch to origin
push_feature() {
    local current_branch=$(git branch --show-current)
    print_info "Pushing branch: $current_branch"

    git push -u origin "$current_branch"
    print_success "Branch pushed to origin"
}

# Merge current branch to master
merge_feature() {
    local current_branch=$(git branch --show-current)

    if [ "$current_branch" = "master" ]; then
        print_error "Cannot merge master to master"
        exit 1
    fi

    print_info "Merging $current_branch to master..."

    # Checkout master
    git checkout master
    git pull origin master

    # Merge feature branch
    git merge "$current_branch"

    # Push to origin
    git push origin master

    print_success "Merged $current_branch to master"

    # Ask if user wants to delete feature branch
    read -p "Delete feature branch $current_branch? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git branch -d "$current_branch"
        git push origin --delete "$current_branch"
        print_success "Deleted feature branch: $current_branch"
    fi
}

# Cleanup merged branches
cleanup() {
    print_info "Cleaning up merged branches..."

    # Get list of merged branches (excluding master)
    local merged_branches=$(git branch --merged master | grep -v "master" | grep -v "^\*")

    if [ -z "$merged_branches" ]; then
        print_info "No merged branches to clean up"
        return
    fi

    echo "$merged_branches" | while read -r branch; do
        print_info "Deleting merged branch: $branch"
        git branch -d "$branch"
        git push origin --delete "$branch" 2>/dev/null || true
    done

    print_success "Cleanup complete"
}

# Show status with branch info
status() {
    local current_branch=$(git branch --show-current)
    local commit_count=$(git rev-list --count master..HEAD 2>/dev/null || echo "0")

    echo -e "${BLUE}Current Branch:${NC} $current_branch"
    echo -e "${BLUE}Commits ahead of master:${NC} $commit_count"
    echo ""
    git status
}

# Undo last commit (keep changes)
undo_last() {
    print_warning "Undoing last commit (keeping changes)..."
    git reset --soft HEAD~1
    print_success "Last commit undone, changes preserved"
}

# Undo last commit (discard changes)
undo_hard() {
    print_warning "This will DISCARD all changes in the last commit!"
    read -p "Are you sure? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git reset --hard HEAD~1
        print_success "Last commit undone, changes discarded"
    else
        print_info "Operation cancelled"
    fi
}

# Main script logic
case "$1" in
    new-feature)
        if [ -z "$2" ]; then
            print_error "Please provide a feature name"
            show_help
            exit 1
        fi
        new_feature "$2"
        ;;
    new-fix)
        if [ -z "$2" ]; then
            print_error "Please provide a fix name"
            show_help
            exit 1
        fi
        new_fix "$2"
        ;;
    save)
        save "$2"
        ;;
    push-feature)
        push_feature
        ;;
    merge-feature)
        merge_feature
        ;;
    cleanup)
        cleanup
        ;;
    status)
        status
        ;;
    undo-last)
        undo_last
        ;;
    undo-hard)
        undo_hard
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
