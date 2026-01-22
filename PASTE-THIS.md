# Copy & Paste Setup

## Step 1: Create Repo on GitHub

1. Go to: https://github.com/new
2. Repository name: `github-contribution-visualizer`
3. Description: `Impact-weighted GitHub contribution visualizer`
4. Make it **Public**
5. **Don't** check "Add a README file" (we already have files)
6. Click **Create repository**

---

## Step 2: Copy & Paste These Commands

**Replace `YOUR_USERNAME` with your actual GitHub username:**

```bash
cd /Users/matthewthompson/Documents/DEVELOPMENT/github-contribution-visualizer

git remote add origin https://github.com/YOUR_USERNAME/github-contribution-visualizer.git

git add .

git commit -m "Add GitHub contribution visualizer"

git push -u origin main
```

**If you get an error about branch name, try:**
```bash
git push -u origin master
```

---

## Step 3: Run Workflow

1. Go to: `https://github.com/YOUR_USERNAME/github-contribution-visualizer`
2. Click **Actions** tab
3. Click **Update Contribution Visualization**
4. Click **Run workflow** → **Run workflow**
5. Wait for green checkmark ✅

---

## Step 4: Add to Profile README

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_USERNAME` (create if needed)
2. Edit `README.md`
3. Add this line (replace `YOUR_USERNAME`):

```markdown
![Contributions](https://raw.githubusercontent.com/YOUR_USERNAME/github-contribution-visualizer/main/contributions-simple.svg)
```

4. Commit and push

---

## Done! 🎉

The chart will auto-update daily.
