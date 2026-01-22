#!/bin/bash
# Automated Setup Script for GitHub Contribution Visualizer
# This script prepares everything and gives you the exact commands to run

set -e

echo "🚀 GitHub Contribution Visualizer - Automated Setup"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Check if files exist
echo ""
echo "📋 Checking required files..."

REQUIRED_FILES=(
    ".github/workflows/update-contributions.yml"
    "generate_contributions_simple.py"
    "generate_contributions.py"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING)"
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo ""
    echo "❌ Missing required files. Please ensure all files are present."
    exit 1
fi

# Check if .gitignore exists and has contributions.svg
if [ -f ".gitignore" ]; then
    if ! grep -q "contributions" .gitignore; then
        echo ""
        echo "📝 Updating .gitignore..."
        echo "" >> .gitignore
        echo "# Contribution visualizer outputs" >> .gitignore
        echo "contributions*.svg" >> .gitignore
        echo "✅ Updated .gitignore"
    fi
else
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Output (will be committed by workflow)
# contributions*.svg

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
    echo "✅ Created .gitignore"
fi

# Get current git remote
echo ""
echo "🔍 Checking git remote..."
if git remote get-url origin &>/dev/null; then
    REMOTE_URL=$(git remote get-url origin)
    echo "  ✅ Remote found: $REMOTE_URL"

    # Extract username and repo from URL
    if [[ $REMOTE_URL =~ github.com[:/]([^/]+)/([^/]+)\.git ]]; then
        GITHUB_USER="${BASH_REMATCH[1]}"
        REPO_NAME="${BASH_REMATCH[2]}"
        echo "  📌 Detected: $GITHUB_USER/$REPO_NAME"
    fi
else
    echo "  ⚠️  No remote configured"
    echo ""
    echo "You'll need to add a remote:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
fi

# Check if files are staged/committed
echo ""
echo "📊 Checking git status..."
if git diff --quiet && git diff --cached --quiet; then
    echo "  ✅ All changes committed"
    NEEDS_COMMIT=false
else
    echo "  ⚠️  Uncommitted changes detected"
    NEEDS_COMMIT=true
fi

# Generate next steps
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "${BLUE}Next Steps:${NC}"
echo ""

if [ "$NEEDS_COMMIT" = true ]; then
    echo "1️⃣  ${YELLOW}Commit and push the files:${NC}"
    echo ""
    echo "   git add .github/workflows/update-contributions.yml"
    echo "   git add generate_contributions_simple.py"
    echo "   git add generate_contributions.py"
    echo "   git add .gitignore"
    echo "   git commit -m 'Add GitHub contribution visualizer'"
    echo "   git push origin main"
    echo ""
fi

echo "2️⃣  ${YELLOW}On GitHub:${NC}"
echo ""
echo "   a) Go to: https://github.com/${GITHUB_USER:-YOUR_USERNAME}/${REPO_NAME:-YOUR_REPO}"
echo "   b) Click 'Actions' tab"
echo "   c) Click 'Update Contribution Visualization'"
echo "   d) Click 'Run workflow' → 'Run workflow'"
echo "   e) Wait for it to complete (green checkmark)"
echo ""

echo "3️⃣  ${YELLOW}Verify the SVG was created:${NC}"
echo ""
echo "   Check that 'contributions-simple.svg' appears in your repo root"
echo "   View it at: https://raw.githubusercontent.com/${GITHUB_USER:-YOUR_USERNAME}/${REPO_NAME:-YOUR_REPO}/main/contributions-simple.svg"
echo ""

echo "4️⃣  ${YELLOW}Add to your profile README:${NC}"
echo ""
echo "   Edit: https://github.com/${GITHUB_USER:-YOUR_USERNAME}/${GITHUB_USER:-YOUR_USERNAME}"
echo ""
echo "   Add this line to README.md:"
echo ""
echo "   ${GREEN}\`\`\`markdown${NC}"
echo "   ![Contributions](https://raw.githubusercontent.com/${GITHUB_USER:-YOUR_USERNAME}/${REPO_NAME:-YOUR_REPO}/main/contributions-simple.svg)"
echo "   ${GREEN}\`\`\`${NC}"
echo ""

echo "5️⃣  ${YELLOW}Done!${NC} The chart will auto-update daily at 00:00 UTC"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
