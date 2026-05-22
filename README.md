# dibi8 Auto Publisher

Automatically publishes articles from [dibi8.com](https://dibi8.com) to multiple social media platforms on a scheduled basis — with built-in anti-ban protections.

## Anti-Ban Safety Features

| Feature | Description |
|---------|-------------|
| **Startup jitter** | Random 0-15 min delay on each run to avoid exact cron timing |
| **Random skip** | 15% chance to skip a run entirely — irregular posting looks human |
| **Per-platform daily caps** | Twitter: 6/day, Facebook: 4/day, LinkedIn: 2/day, Medium: 1/day, Reddit: 2/day |
| **Minimum intervals** | Enforced cooldown between posts (Twitter 2h, LinkedIn 6h, Medium 24h, Reddit 8h) |
| **Inter-platform delays** | 1-5 min random wait between posting to different platforms |
| **Content variation** | Different post format/template per platform, random hashtags, varied hooks |
| **Shuffled platform order** | Platforms are published in random order each run |
| **Token validation** | Credentials are checked before publishing; expired tokens logged |
| **Retry with backoff** | Exponential backoff on rate-limit errors (not blind retry) |
| **Reddit-specific** | Subreddit rotation, duplicate URL detection, varied title prefixes |
| **User-Agent rotation** | Random browser UA for web scraping |
| **Weighted article selection** | Newer articles are more likely to be picked |

## Features

- **RSS-based scraping** — fetches articles from dibi8.com's RSS feed (257+ articles)
- **Multi-platform publishing** — Twitter/X, Facebook, LinkedIn, Medium, Reddit
- **Smart scheduling** — runs every hour during business hours in both Asia and US timezones
- **Duplicate prevention** — tracks published articles per platform in `data/published.json`
- **Auto-reset** — when all articles have been published, resets and starts cycling again
- **Graceful degradation** — unconfigured platforms are silently skipped

## Schedule

| Region | Local Time | UTC |
|--------|-----------|-----|
| Asia (UTC+8) | 09:00 – 17:00 | 01:00 – 09:00 |
| US (UTC-5) | 09:00 – 17:00 | 14:00 – 22:00 |

The workflow runs **every hour** during these windows = **18 cron triggers/day**.
With random skips (~15%) and rate limits, actual posts per platform are much lower.

## Quick Start

1. **Fork/clone** this repository
2. **Set up API keys** — follow [API_SETUP_GUIDE.md](./API_SETUP_GUIDE.md)
3. **Add secrets** to your GitHub repository settings
4. The GitHub Action will start running automatically on schedule

### Manual Run

```bash
pip install -r requirements.txt

# Disable delays for local testing
export STARTUP_JITTER_MAX=0
export INTER_PLATFORM_DELAY_MIN=0
export INTER_PLATFORM_DELAY_MAX=0
export RANDOM_SKIP_PROBABILITY=0

# Set platform credentials
export TWITTER_API_KEY="..."
# ... (see API_SETUP_GUIDE.md for all variables)

python run.py
```

## Project Structure

```
├── .github/workflows/
│   └── auto-publish.yml     # GitHub Actions scheduled workflow
├── src/
│   ├── config.py            # Configuration & environment variables
│   ├── scraper.py           # RSS feed parser & article metadata scraper
│   ├── scheduler.py         # Main orchestrator with safety controls
│   ├── safety.py            # Rate limiting, daily caps, cooldowns, jitter
│   ├── content.py           # Content variation engine (per-platform formatting)
│   └── publishers/
│       ├── twitter.py       # Twitter/X via Tweepy + retry + rate-limit handling
│       ├── facebook.py      # Facebook Page via Graph API + token expiry detection
│       ├── linkedin.py      # LinkedIn via REST API v2 + token expiry detection
│       ├── medium.py        # Medium via Integration Token + retry
│       └── reddit.py        # Reddit via PRAW + duplicate detection + subreddit rotation
├── data/
│   ├── published.json       # Tracks published article URLs per platform
│   └── rate_limits.json     # Tracks daily post counts and last-post timestamps
├── requirements.txt
├── API_SETUP_GUIDE.md       # Step-by-step API key setup guide
└── README.md
```

## Configuration

All configuration is via environment variables (or GitHub Secrets).

### Anti-Ban Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `STARTUP_JITTER_MAX` | `900` | Max random startup delay in seconds (0-15 min) |
| `INTER_PLATFORM_DELAY_MIN` | `60` | Min delay between platform posts (seconds) |
| `INTER_PLATFORM_DELAY_MAX` | `300` | Max delay between platform posts (seconds) |
| `RANDOM_SKIP_PROBABILITY` | `0.15` | Probability (0-1) to skip a run entirely |

### Platform Credentials

| Platform | Required Secrets |
|----------|-----------------|
| Twitter/X | `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET` |
| Facebook | `FACEBOOK_PAGE_ID`, `FACEBOOK_ACCESS_TOKEN` |
| LinkedIn | `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_ORG_ID` (optional) |
| Medium | `MEDIUM_TOKEN` |
| Reddit | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`, `REDDIT_SUBREDDITS` |

### Reddit Multi-Subreddit

Set `REDDIT_SUBREDDITS` to a comma-separated list to rotate between subreddits:

```
REDDIT_SUBREDDITS=artificial,MachineLearning,OpenSource,selfhosted
```

## Avoiding Account Bans: Best Practices

1. **Start slow** — Don't enable all platforms at once. Start with 1-2 and add more over weeks.
2. **Engage manually** — Especially on Reddit, make sure your account has genuine activity (comments, upvotes) beyond auto-posts.
3. **Monitor logs** — Check GitHub Actions logs regularly for warnings about rate limits or expired tokens.
4. **LinkedIn tokens expire** — LinkedIn OAuth tokens expire every 60 days. Set a calendar reminder.
5. **Facebook Page tokens** — Use a Page Access Token (never expires) rather than a User Access Token (expires in 60 days).
6. **Reddit karma** — Build up account karma before enabling auto-posting. Low-karma accounts are flagged more easily.
7. **Don't run on weekends** — Consider disabling weekend runs for LinkedIn (add `1-5` to cron day-of-week).

## License

MIT
