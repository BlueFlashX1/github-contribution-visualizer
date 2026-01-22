#!/bin/bash
# Test the contribution visualizer locally before pushing to GitHub
# Requires: GITHUB_TOKEN and GITHUB_USERNAME environment variables

set -e

echo "🧪 Testing Contribution Visualizer Locally"
echo "==========================================="
echo ""

# Check for required environment variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN not set"
    echo ""
    echo "To test locally, you need a GitHub Personal Access Token:"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Generate new token (classic)"
    echo "  3. Select scope: public_repo"
    echo "  4. Copy the token"
    echo ""
    echo "Then run:"
    echo "  export GITHUB_TOKEN=ghp_your_token_here"
    echo "  export GITHUB_USERNAME=your_username"
    echo "  ./test-local.sh"
    echo ""
    exit 1
fi

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GITHUB_USERNAME not set"
    echo ""
    echo "Run: export GITHUB_USERNAME=your_username"
    echo ""
    exit 1
fi

echo "✅ Token and username configured"
echo "   Username: $GITHUB_USERNAME"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -q PyGithub

echo ""
echo "🚀 Running contribution visualizer..."
echo ""

python3 generate_contributions_simple.py

echo ""
if [ -f "contributions-simple.svg" ]; then
    echo "✅ Success! Generated contributions-simple.svg"
    echo ""
    echo "📊 Preview the SVG:"
    echo "   Open: contributions-simple.svg"
    echo ""
    echo "💡 If it looks good, you're ready to push to GitHub!"
else
    echo "❌ Error: SVG file not generated"
    exit 1
fi
