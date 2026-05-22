"""Twitter/X publisher using Tweepy."""

import logging

import tweepy

from .. import config
from ..scraper import Article

logger = logging.getLogger(__name__)


def is_configured() -> bool:
    return all([
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET,
        config.TWITTER_ACCESS_TOKEN,
        config.TWITTER_ACCESS_SECRET,
    ])


def publish(article: Article) -> bool:
    """Post an article to Twitter/X."""
    if not is_configured():
        logger.warning("Twitter not configured, skipping")
        return False

    try:
        client = tweepy.Client(
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_SECRET,
        )

        hashtags = " ".join(config.DEFAULT_HASHTAGS[:3])
        tweet_text = f"{article.title}\n\n{article.description[:180]}...\n\n{article.url}\n\n{hashtags}"

        # Twitter limit is 280 chars
        if len(tweet_text) > 280:
            max_desc = 280 - len(article.title) - len(article.url) - len(hashtags) - 12
            if max_desc > 0:
                tweet_text = f"{article.title}\n\n{article.description[:max_desc]}...\n\n{article.url}\n\n{hashtags}"
            else:
                tweet_text = f"{article.title}\n\n{article.url}\n\n{hashtags}"
                if len(tweet_text) > 280:
                    tweet_text = f"{article.title[:200]}\n\n{article.url}"

        client.create_tweet(text=tweet_text)
        logger.info("Successfully posted to Twitter: %s", article.title)
        return True

    except Exception:
        logger.exception("Failed to post to Twitter")
        return False
