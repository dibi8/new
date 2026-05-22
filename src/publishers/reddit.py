"""Reddit publisher using PRAW."""

import logging

import praw

from .. import config
from ..scraper import Article

logger = logging.getLogger(__name__)


def is_configured() -> bool:
    return all([
        config.REDDIT_CLIENT_ID,
        config.REDDIT_CLIENT_SECRET,
        config.REDDIT_USERNAME,
        config.REDDIT_PASSWORD,
    ])


def publish(article: Article) -> bool:
    """Post an article link to Reddit."""
    if not is_configured():
        logger.warning("Reddit not configured, skipping")
        return False

    try:
        reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            username=config.REDDIT_USERNAME,
            password=config.REDDIT_PASSWORD,
            user_agent="dibi8-auto-publisher/1.0",
        )

        subreddit = reddit.subreddit(config.REDDIT_SUBREDDIT)
        subreddit.submit(
            title=article.title,
            url=article.url,
        )
        logger.info("Successfully posted to Reddit r/%s: %s", config.REDDIT_SUBREDDIT, article.title)
        return True

    except Exception:
        logger.exception("Failed to post to Reddit")
        return False
