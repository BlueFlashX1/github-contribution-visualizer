# Top Languages Card Setup

## Current Status

The languages card currently works with **public repos only** using the default `GITHUB_TOKEN`.

## To Include Private Repos

To show languages from both **public and private** repositories, you need to create a Personal Access Token (PAT):

### Step 1: Create Personal Access Token

1. Go to: <https://github.com/settings/tokens>
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it: `github-contribution-visualizer`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `public_repo` (Access public repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)

### Step 2: Add Token as Secret

1. Go to your repository: <https://github.com/BlueFlashX1/github-contribution-visualizer>
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `PAT_TOKEN`
5. Value: Paste your token
6. Click **Add secret**

### Step 3: Update Workflow

Edit `.github/workflows/update-languages.yml`:

Change this line:

```yaml
GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

To:

```yaml
GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}
```

### Step 4: Trigger Workflow

1. Go to: <https://github.com/BlueFlashX1/github-contribution-visualizer/actions>
2. Click "Update Languages Card" → "Run workflow"

The card will now include languages from both public and private repositories.

## Security Note

- PAT tokens have access to your private repos
- Keep the token secret
- If compromised, revoke it immediately in Settings → Developer settings → Personal access tokens
