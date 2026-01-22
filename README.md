# GitHub Contribution Visualizer

Impact-weighted contribution graph showing real contributions based on PRs, reviews, and issues—not just commit frequency.

## Features

- **Impact-Weighted**: PRs merged (5pts), PRs opened (3pts), Reviews (2pts), Issues (1pt)
- **Real Contributions**: Shows meaningful work, not commit spam
- **Auto-Updates**: Runs hourly via GitHub Actions
- **Easy to Embed**: Simple markdown image tag for profile READMEs

## Why This Exists

The standard GitHub contribution graph only shows commit frequency, which rewards noise over signal and ignores code reviews, PRs, and issues. This tool shows what actually matters: merged PRs, helpful reviews, and meaningful issues.

## Quick Start

### GitHub Action (Recommended)

1. Fork this repository or add the workflow to your existing repo

2. **Token Setup**:
   - Public repos only: No setup needed. GitHub provides token automatically
   - Private repos: See [SETUP.md](SETUP.md) for Personal Access Token instructions

3. **Choose your style**:
   - Card style (default): `generate_contributions_simple.py`
   - Heatmap style: `generate_contributions.py`

   Edit `.github/workflows/update-contributions.yml` to switch styles.

4. **Run the workflow**:
   - Runs automatically every hour
   - Or trigger manually: Actions → "Update Contribution Visualization" → Run workflow

5. **Embed in your profile README**:

   ```markdown
   ![Contributions](https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/contributions-simple.svg)
   ```

### Local Script

1. Install dependencies:

   ```bash
   pip install PyGithub
   ```

2. Create GitHub Personal Access Token:
   - Go to: GitHub Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - Scopes needed: `public_repo` (or `repo` for private repos)
   - See [SETUP.md](SETUP.md) for detailed instructions

3. Set environment variables:

   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   export GITHUB_USERNAME=your_username
   ```

4. Run the script:

   ```bash
   python generate_contributions_simple.py
   ```

5. Output: `contributions-simple.svg` will be generated

## What It Shows

- **PRs Merged** (5 points): High-impact contributions
- **PRs Opened** (3 points): Active development
- **PRs Reviewed** (2 points): Collaboration and code quality
- **Issues** (1 point): Community engagement

Not included: Raw commit count (which can be gamed)

## Visualization Styles

### Card Style (Default)

Clean card layout with large numbers. Four metric boxes: PRs Merged, PRs Opened, Reviews, Issues. Impact score bar at the bottom. Perfect for profile READMEs.

### Heatmap Style

Year-long heatmap grid showing daily activity patterns. More detailed but requires more space.

## Update Frequency

- Runs hourly automatically
- Updates on repository events (push, PR, issues)
- Daily backup at 00:00 UTC

See [REALTIME-SETUP.md](REALTIME-SETUP.md) for advanced real-time configuration.

## Customization

Edit `generate_contributions_simple.py` to customize:

- Colors: Change the color palette
- Scoring: Adjust point values in `get_metrics()`
- Time Range: Change `days=365` parameter
- Style: Modify SVG generation in `generate_card_svg()`

## Privacy & Security

- Uses GitHub's official API
- Only accesses public repository data
- No data is stored or transmitted outside GitHub
- Token is only used for API authentication

## Contributing

Improvements welcome:

- Visualization design enhancements
- Additional contribution types (documentation, discussions, etc.)
- API call optimization
- Private repo support (with proper permissions)

## License

MIT License - Use freely for your own profile.

---

The greener graph doesn't indicate the better developer. This tool shows the developer who makes meaningful contributions.
