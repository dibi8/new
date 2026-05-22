# dibi8 Auto Publisher

Automatically publishes articles from [dibi8.com](https://dibi8.com) to multiple social media platforms on a scheduled basis.

## Features

- **RSS-based scraping** — fetches articles from dibi8.com's RSS feed (257+ articles)
- **Multi-platform publishing** — Twitter/X, Facebook, LinkedIn, Medium, Reddit
- **Smart scheduling** — runs every hour during business hours in both Asia and US timezones
- **Duplicate prevention** — tracks published articles per platform in `data/published.json`
- **Auto-reset** — when all articles have been published, resets and starts cycling again
- **Random selection** — picks a random unpublished article each run for variety
- **Graceful degradation** — unconfigured platforms are silently skipped

## Schedule

| Region | Local Time | UTC |
|--------|-----------|-----|
| Asia (UTC+8) | 09:00 – 17:00 | 01:00 – 09:00 |
| US (UTC-5) | 09:00 – 17:00 | 14:00 – 22:00 |

The workflow runs **every hour** during these windows = **18 runs/day**.

## Quick Start

1. **Fork/clone** this repository
2. **Set up API keys** — follow [API_SETUP_GUIDE.md](./API_SETUP_GUIDE.md)
3. **Add secrets** to your GitHub repository settings
4. The GitHub Action will start running automatically on schedule

### Manual Run

```bash
pip install -r requirements.txt

# Set environment variables for the platforms you want
export TWITTER_API_KEY="..."
export TWITTER_API_SECRET="..."
export TWITTER_ACCESS_TOKEN="..."
export TWITTER_ACCESS_SECRET="..."
# ... (see API_SETUP_GUIDE.md for all variables)

python run.py
```

### Trigger via GitHub Actions

Go to **Actions** → **Auto Publish dibi8 Articles** → **Run workflow**

## Project Structure

```
├── .github/workflows/
│   └── auto-publish.yml     # GitHub Actions scheduled workflow
├── src/
│   ├── config.py            # Configuration & environment variables
│   ├── scraper.py           # RSS feed parser & article metadata scraper
│   ├── scheduler.py         # Main orchestrator
│   └── publishers/
│       ├── twitter.py       # Twitter/X via Tweepy
│       ├── facebook.py      # Facebook Page via Graph API
│       ├── linkedin.py      # LinkedIn via REST API v2
│       ├── medium.py        # Medium via Integration Token
│       └── reddit.py        # Reddit via PRAW
├── data/
│   └── published.json       # Tracks published article URLs per platform
├── requirements.txt
├── API_SETUP_GUIDE.md       # Step-by-step API key setup guide
└── README.md
```

## Configuration

All configuration is via environment variables (or GitHub Secrets). See [API_SETUP_GUIDE.md](./API_SETUP_GUIDE.md) for detailed setup instructions.

| Platform | Required Secrets |
|----------|-----------------|
| Twitter/X | `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET` |
| Facebook | `FACEBOOK_PAGE_ID`, `FACEBOOK_ACCESS_TOKEN` |
| LinkedIn | `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_ORG_ID` (optional) |
| Medium | `MEDIUM_TOKEN` |
| Reddit | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`, `REDDIT_SUBREDDIT` |

## License

MIT
