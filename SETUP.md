# Token Configuration Guide

## Two Scenarios

### Scenario 1: GitHub Actions (Automatic - Recommended)

**Good news**: You don't need to create a token! GitHub Actions provides one automatically.

The workflow uses `secrets.GITHUB_TOKEN` which is:
- ✅ Automatically provided by GitHub
- ✅ No setup required
- ✅ Has read access to public repos
- ✅ Limited scope (can't access private repos without extra permissions)

**What you need to do**: Nothing! Just push the workflow file and it works.

**Limitation**: If you want to include private repo contributions, you'll need a Personal Access Token (see Scenario 2).

---

### Scenario 2: Local Script or Private Repos

If you're running the script locally OR want to include private repo data, you need a **Personal Access Token (PAT)**.

## Step-by-Step: Create Personal Access Token

### 1. Go to GitHub Settings

1. Click your profile picture (top right)
2. Click **Settings**
3. Scroll down to **Developer settings** (bottom left)
4. Click **Personal access tokens**
5. Click **Tokens (classic)** or **Fine-grained tokens**

### 2. Create New Token

**Option A: Classic Token (Simpler)**

1. Click **Generate new token** → **Generate new token (classic)**
2. Give it a name: `Contribution Visualizer`
3. Set expiration: `90 days` (or `No expiration` if you prefer)
4. **Select scopes** (permissions):
   - ✅ `public_repo` - Read public repositories
   - ✅ `repo` - Full control of private repositories (if you have private repos)
5. Click **Generate token**
6. **COPY THE TOKEN IMMEDIATELY** - You won't see it again!

**Option B: Fine-Grained Token (More Secure)**

1. Click **Generate new token** → **Generate new token (fine-grained)**
2. Give it a name: `Contribution Visualizer`
3. Set expiration: `90 days`
4. **Repository access**: 
   - Select **Only select repositories** (if you have private repos)
   - Or **All repositories** (if you want everything)
5. **Repository permissions**:
   - ✅ `Contents: Read` - Read repository contents
   - ✅ `Issues: Read` - Read issues
   - ✅ `Pull requests: Read` - Read pull requests
   - ✅ `Metadata: Read` - Read repository metadata (always enabled)
6. Click **Generate token**
7. **COPY THE TOKEN IMMEDIATELY**

### 3. Use the Token

**For Local Script:**

```bash
export GITHUB_TOKEN=ghp_your_token_here
export GITHUB_USERNAME=your_username
python generate_contributions_simple.py
```

**For GitHub Actions (if you need private repo access):**

1. Go to your repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GITHUB_TOKEN` (or `PAT_TOKEN`)
5. Value: Paste your Personal Access Token
6. Click **Add secret**

Then update the workflow:

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}  # Use your PAT instead of default
  GITHUB_USERNAME: ${{ github.repository_owner }}
```

---

## Required Permissions Summary

### Minimum (Public Repos Only)
- `public_repo` (classic) OR `Contents: Read` (fine-grained)
- `Metadata: Read` (always enabled)

### Recommended (Includes Private Repos)
- `repo` (classic) OR `Contents: Read` + `Issues: Read` + `Pull requests: Read` (fine-grained)

### What Each Permission Does

| Permission | What It Accesses |
|------------|------------------|
| `public_repo` | Public repositories only |
| `repo` | All repositories (public + private) |
| `Contents: Read` | Read repository code and files |
| `Issues: Read` | Read issues (for issue metrics) |
| `Pull requests: Read` | Read PRs (for PR metrics) |

---

## Security Best Practices

1. **Never commit tokens to git**
   - Use environment variables
   - Use GitHub Secrets for Actions
   - Add `.env` to `.gitignore`

2. **Use minimum permissions**
   - Only grant what's needed
   - Fine-grained tokens are more secure

3. **Set expiration dates**
   - Rotate tokens regularly
   - Revoke unused tokens

4. **For GitHub Actions**
   - Default `GITHUB_TOKEN` is automatically scoped
   - Only use PAT if you need private repo access

---

## Quick Reference

### GitHub Actions (Default - No Setup)
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Auto-provided
```

### GitHub Actions (Private Repos)
```yaml
env:
  GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}  # Your Personal Access Token
```

### Local Script
```bash
export GITHUB_TOKEN=ghp_your_token_here
python generate_contributions_simple.py
```

---

## Troubleshooting

**Error: "Bad credentials"**
- Token is invalid or expired
- Check token hasn't been revoked
- Regenerate if needed

**Error: "Resource not accessible by integration"**
- Token doesn't have required permissions
- Add `repo` scope for private repos

**Error: "API rate limit exceeded"**
- GitHub API has rate limits
- Authenticated requests have higher limits
- Wait a bit and try again

**No data showing**
- Check token has access to the repositories
- Verify repositories are not archived
- Check date range (default is last 365 days)
