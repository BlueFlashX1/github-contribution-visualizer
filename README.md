# GitHub Contribution Visualizer

A beautiful, impact-weighted contribution graph that shows **real contributions** based on PRs, reviews, and issues—not just commit frequency.

## ✨ Features

- **Impact-Weighted**: PRs merged (5pts), PRs opened (3pts), Reviews (2pts), Issues (1pt)
- **Real Contributions**: Shows actual meaningful work, not just commit spam
- **Beautiful Design**: Modern, readable SVG visualization
- **Auto-Updates**: GitHub Action runs daily to keep it current
- **Easy to Embed**: Simple markdown image tag for your profile README

## 🎯 Why This Exists

The standard GitHub contribution graph only shows commit frequency, which:

- Rewards noise over signal (20 typo fixes > 1 architecture design)
- Ignores code reviews, PRs, and issues
- Doesn't reflect actual impact or collaboration

This tool shows **what actually matters**: merged PRs, helpful reviews, and meaningful issues.

## 🚀 Quick Start

### Option 1: GitHub Action (Recommended)

1. **Fork this repository** or add the workflow to your existing repo

2. **Token Setup** (usually no action needed!):
   - ✅ **Public repos only**: No setup needed! GitHub provides token automatically
   - 🔒 **Private repos**: See [SETUP.md](SETUP.md) for Personal Access Token instructions

3. **Choose your style**:
   - **Card style** (default, simple & readable): `generate_contributions_simple.py`
   - **Heatmap style** (detailed year view): `generate_contributions.py`
   
   Edit `.github/workflows/update-contributions.yml` to switch styles.

4. **Run the workflow**:
   - It will run automatically daily
   - Or trigger manually: Actions → "Update Contribution Visualization" → Run workflow

5. **Embed in your profile README**:

   ```markdown
   ![Contributions](https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/contributions-simple.svg)
   ```

### Option 2: Local Script

1. **Install dependencies**:

   ```bash
   pip install PyGithub requests
   ```

2. **Create GitHub Personal Access Token**:
   - Go to: GitHub Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Scopes needed: `public_repo` (or `repo` for private repos)
   - See [SETUP.md](SETUP.md) for detailed instructions

3. **Set environment variables**:

   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   export GITHUB_USERNAME=your_username
   ```

4. **Run the script** (choose one):

   ```bash
   # Simple card style (recommended - easier to read)
   python generate_contributions_simple.py
   
   # Or detailed heatmap style
   python generate_contributions.py
   ```

5. **Output**: `contributions-simple.svg` or `contributions.svg` will be generated

## 📊 What It Shows

The visualization displays:

- **PRs Merged** (5 points): High-impact contributions
- **PRs Opened** (3 points): Active development
- **PRs Reviewed** (2 points): Collaboration and code quality
- **Issues Opened/Closed** (1 point): Community engagement

**Not included**: Raw commit count (which can be gamed)

## 🎨 Customization

Edit `generate_contributions.py` to customize:

- **Colors**: Change the `colors` dictionary
- **Scoring**: Adjust point values in `get_contribution_metrics()`
- **Time Range**: Change `days=365` parameter
- **Style**: Modify SVG generation in `generate_svg()`

## 📝 Two Visualization Styles

### Card Style (Simple & Readable)
- Clean card layout with large, readable numbers
- Four metric boxes: PRs Merged, PRs Opened, Reviews, Issues
- Impact score bar at the bottom
- Perfect for profile READMEs - easy to understand at a glance

### Heatmap Style (Detailed)
- Year-long heatmap grid (like GitHub's graph)
- Shows daily activity patterns
- Month labels and day labels
- More detailed but requires more space

**Recommendation**: Start with the card style - it's easier to read and understand!

## 🔒 Privacy & Security

- Uses GitHub's official API
- Only accesses public repository data
- No data is stored or transmitted outside GitHub
- Token is only used for API authentication

## 🤝 Contributing

Feel free to:

- Improve the visualization design
- Add more contribution types (documentation, discussions, etc.)
- Optimize API calls for better performance
- Add support for private repos (with proper permissions)

## 📄 License

MIT License - Use freely for your own profile!

---

**Remember**: The greener graph doesn't indicate the better developer.  
**This tool** shows the developer who makes meaningful contributions.
