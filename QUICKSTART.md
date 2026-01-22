# Quick Start Guide

I've automated everything I can. Here's what's done and what you need to do:

## ✅ What I've Done For You

- ✅ Created all required files
- ✅ Configured the GitHub Action workflow
- ✅ Set up `.gitignore` properly
- ✅ Created automated setup script
- ✅ Created local testing script
- ✅ Everything is ready to push

## 🚀 What You Need To Do (3 Steps)

### Step 1: Create GitHub Repo (if needed)

**If you don't have a repo yet:**

1. Go to: <https://github.com/new>
2. Repository name: `github-contribution-visualizer` (or any name you want)
3. Make it **Public** (or Private, but then you'll need a PAT token)
4. **Don't** initialize with README (we already have files)
5. Click **Create repository**

**If you already have a repo:**

- Skip this step, just note the repo URL

---

### Step 2: Push to GitHub

Run these commands (replace `YOUR_USERNAME` with your GitHub username):

```bash
cd /Users/matthewthompson/Documents/DEVELOPMENT/github-contribution-visualizer

# Add remote (replace YOUR_USERNAME and repo name)
git remote add origin https://github.com/YOUR_USERNAME/github-contribution-visualizer.git

# Stage all files
git add .

# Commit
git commit -m "Add GitHub contribution visualizer"

# Push
git push -u origin main
```

**Note:** If your default branch is `master` instead of `main`, use:

```bash
git push -u origin master
```

---

### Step 3: Run the Workflow

1. Go to your repo on GitHub: `https://github.com/YOUR_USERNAME/github-contribution-visualizer`
2. Click the **Actions** tab
3. Click **Update Contribution Visualization** (left sidebar)
4. Click **Run workflow** button (top right)
5. Click **Run workflow** again in the dropdown
6. Wait ~30 seconds for it to complete (watch the progress)
7. When you see a green checkmark ✅, it's done!

---

### Step 4: Add to Your Profile

1. Go to your profile repo: `https://github.com/YOUR_USERNAME/YOUR_USERNAME`
   - If it doesn't exist, create it (same name as your username)
2. Edit `README.md` (or create it)
3. Add this line (replace `YOUR_USERNAME`):

```markdown
![Contributions](https://raw.githubusercontent.com/YOUR_USERNAME/github-contribution-visualizer/main/contributions-simple.svg)
```

4. Commit and push
5. Check your profile - the chart should appear!

---

## 🧪 Optional: Test Locally First

Want to see what it looks like before pushing?

```bash
cd /Users/matthewthompson/Documents/DEVELOPMENT/github-contribution-visualizer

# Get a token from: https://github.com/settings/tokens
# Select scope: public_repo
export GITHUB_TOKEN=ghp_your_token_here
export GITHUB_USERNAME=your_username

# Run the test
./test-local.sh
```

This will generate `contributions-simple.svg` locally so you can preview it.

---

## 📋 Checklist

- [ ] Created GitHub repo (or have existing repo)
- [ ] Added remote: `git remote add origin https://github.com/YOUR_USERNAME/REPO.git`
- [ ] Pushed files: `git push -u origin main`
- [ ] Ran workflow in GitHub Actions
- [ ] Verified `contributions-simple.svg` exists in repo
- [ ] Added image link to profile README
- [ ] Checked profile - chart appears!

---

## 🆘 Troubleshooting

**"Repository not found"**

- Check the repo name and your username
- Make sure the repo exists on GitHub

**"Workflow failed"**

- Check the Actions tab → failed run → Logs
- Make sure you're using the correct branch name (`main` vs `master`)

**"Image doesn't show"**

- Check the raw URL: `https://raw.githubusercontent.com/USER/REPO/main/contributions-simple.svg`
- Make sure the branch name matches (`main` or `master`)
- Wait a few seconds for GitHub to update

**"No contributions showing"**

- The script only counts public repos
- If you have few public repos, numbers may be low
- This is normal if most of your work is in private repos

---

## 🎉 Done

Once set up, the chart will **auto-update daily at 00:00 UTC**. No further action needed!
