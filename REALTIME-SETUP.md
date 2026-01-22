# Real-Time Update Setup

The workflow now updates automatically when you have GitHub activity!

## How It Works

The workflow triggers on:

1. **Repository Events** (Real-time):
   - `push` - When you push code
   - `pull_request` - When PRs are opened/closed/merged
   - `issues` - When issues are opened/closed
   - `issue_comment` - When you comment on issues/PRs

2. **Daily Backup**:
   - Still runs at 00:00 UTC daily (in case events are missed)

3. **Manual Trigger**:
   - Can still be triggered manually from Actions tab

## Important Note

**The workflow triggers on events in THIS repository** (`github-contribution-visualizer`).

To update when you have activity in OTHER repositories, you have two options:

### Option 1: More Frequent Schedule (Simplest)

Change the schedule to run more often:

```yaml
schedule:
  - cron: '0 * * * *'  # Every hour
  # or
  - cron: '*/30 * * * *'  # Every 30 minutes
```

**Pros**: Simple, no setup
**Cons**: Not truly real-time, runs even when no activity

### Option 2: Webhook Setup (True Real-Time)

Set up webhooks on your other repositories to trigger this workflow:

1. **Go to each repo you want to track**:
   - Settings → Webhooks → Add webhook

2. **Webhook settings**:
   - Payload URL: `https://api.github.com/repos/BlueFlashX1/github-contribution-visualizer/dispatches`
   - Content type: `application/json`
   - Secret: (optional, but recommended)
   - Events: Select:
     - Pull requests
     - Issues
     - Issue comments
     - Pushes

3. **Add webhook secret to this repo**:
   - Go to: Settings → Secrets → Actions
   - Add secret: `WEBHOOK_SECRET` (same value you used in webhook)

4. **Update workflow** to verify webhook secret (optional but recommended)

**Pros**: True real-time updates
**Cons**: Requires setup for each repo you want to track

### Option 3: Repository Dispatch API (Programmatic)

You can trigger updates programmatically from any repo:

```bash
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/BlueFlashX1/github-contribution-visualizer/dispatches \
  -d '{"event_type":"update-contributions"}'
```

**Pros**: Full control, can trigger from anywhere
**Cons**: Requires API token, manual setup

## Recommended Approach

**For most users**: The current setup (repository events + daily backup) is perfect!

- Updates when you push to THIS repo
- Updates when you create PRs/issues in THIS repo
- Daily backup ensures nothing is missed
- No additional setup needed

**For tracking ALL repos**: Use Option 1 (hourly schedule) - simplest and most reliable.

**For true real-time across repos**: Use Option 2 (webhooks) - requires more setup but gives instant updates.

## Current Behavior

With the current setup, the chart will update:

- ✅ When you push code to `github-contribution-visualizer` repo
- ✅ When you create/merge PRs in `github-contribution-visualizer` repo
- ✅ When you open/close issues in `github-contribution-visualizer` repo
- ✅ Daily at 00:00 UTC (backup)
- ✅ Manually via Actions tab

**Note**: Events in OTHER repositories won't trigger this workflow automatically. Use one of the options above if you want to track all repos.
