"""Configuration for the auto-publisher."""

import os

# dibi8.com RSS feed
RSS_FEED_URL = "https://dibi8.com/index.xml"
SITE_BASE_URL = "https://dibi8.com"

# Published articles tracking file
PUBLISHED_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "published.json")

# Number of articles to publish per run
ARTICLES_PER_RUN = 1

# Hashtags to include in posts
DEFAULT_HASHTAGS = ["#AI", "#OpenSource", "#DevTools", "#MachineLearning", "#LLM"]

# --- Twitter/X ---
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET", "")

# --- Facebook ---
FACEBOOK_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "")
FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")

# --- LinkedIn ---
LINKEDIN_ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_ORG_ID = os.environ.get("LINKEDIN_ORG_ID", "")

# --- Medium ---
MEDIUM_TOKEN = os.environ.get("MEDIUM_TOKEN", "")

# --- Reddit ---
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET", "")
REDDIT_USERNAME = os.environ.get("REDDIT_USERNAME", "")
REDDIT_PASSWORD = os.environ.get("REDDIT_PASSWORD", "")
REDDIT_SUBREDDIT = os.environ.get("REDDIT_SUBREDDIT", "artificial")
