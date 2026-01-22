# Setup Instructions (Public Repos Only)

No token required. Follow these steps.

---

## Step 1: Create or Use a Repo

**Option A – Use this repo as-is**

- The project lives at `github-contribution-visualizer`.
- Use it in your main profile repo **or** any repo you want the chart to live in.

**Option B – Dedicated “charts” repo**

- Create a new repo, e.g. `github-contribution-visualizer` or `my-contribution-charts`.
- Copy into it:
  - `generate_contributions_simple.py`
  - `generate_contributions.py` (optional, for heatmap)
  - `.github/workflows/update-contributions.yml`
  - `README.md` (optional)

---

## Step 2: Push the Workflow

1. Ensure `.github/workflows/update-contributions.yml` exists in the repo.
2. Commit and push:

   ```bash
   cd /path/to/github-contribution-visualizer
   git add .github/workflows/update-contributions.yml generate_contributions_simple.py
   git commit -m "Add contribution visualizer workflow"
   git push
   ```

---

## Step 3: Run the Workflow

1. Open the repo on GitHub.
2. Go to **Actions**.
3. Select **Update Contribution Visualization**.
4. Click **Run workflow** → **Run workflow**.
5. Wait for the run to finish (green check).

---

## Step 4: Confirm the SVG Exists

1. Go to the repo **Code** tab.
2. Check that `contributions-simple.svg` appears in the root.
3. Open it to confirm it shows your public contribution metrics.

---

## Step 5: Embed in Your Profile README

1. Open your **profile README** repo:  
   `https://github.com/YOUR_USERNAME/YOUR_USERNAME`
2. Edit `README.md`.
3. Add this line (replace `YOUR_USERNAME` and `YOUR_REPO`):

   ```markdown
   ![Contributions](https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/contributions-simple.svg)
   ```

   Examples:

   - Repo `github-contribution-visualizer` under `matthewthompson`:

     ```markdown
     ![Contributions](https://raw.githubusercontent.com/matthewthompson/github-contribution-visualizer/main/contributions-simple.svg)
     ```

   - Repo `my-charts` under `matthewthompson`:

     ```markdown
     ![Contributions](https://raw.githubusercontent.com/matthewthompson/my-charts/main/contributions-simple.svg)
     ```

4. Commit and push. The image will show up on your profile.

---

## Step 6: Let It Auto-Update

- The workflow runs **daily at 00:00 UTC**.
- No extra steps. The chart updates automatically.

---

## Summary

| Step | Action |
|------|--------|
| 1 | Create/use repo with workflow + scripts |
| 2 | Push `.github/workflows/update-contributions.yml` and `generate_contributions_simple.py` |
| 3 | Actions → **Update Contribution Visualization** → **Run workflow** |
| 4 | Confirm `contributions-simple.svg` in repo root |
| 5 | Add image link to profile README |
| 6 | Daily runs keep it updated |

---

## Troubleshooting

**Workflow fails**

- Ensure the default branch is `main` (or update the workflow’s `git push` if you use `master`).
- Check **Actions** → **Update Contribution Visualization** → failed run → **Logs**.
- If push is denied, the workflow uses `contents: write`. In org repos, check **Settings** → **Actions** → **General** → **Workflow permissions** allows read and write.

**SVG is empty or wrong**

- The script uses **public** repos only. If you have few public repos, numbers may be low.
- `GITHUB_USERNAME` comes from the repo owner; the workflow uses `github.repository_owner`. Using the same account that owns the repo is correct.

**Image doesn’t appear in README**

- Confirm the URL:  
  `https://raw.githubusercontent.com/USER/REPO/main/contributions-simple.svg`
- Replace `USER`, `REPO`, and `main` if your default branch differs.
- Save and push the README; give it a few seconds to refresh.

---

**Public repos only – no token or secrets required.**
