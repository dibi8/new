"""Twitter/X publisher using Tweepy with anti-ban protections."""

import logging
import time

import tweepy

from .. import config
from ..scraper import Article
from ..content import format_twitter
from ..safety import can_post, record_post

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def is_configured() -> bool:
    return all([
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET,
        config.TWITTER_ACCESS_TOKEN,
        config.TWITTER_ACCESS_SECRET,
    ])


def validate_credentials() -> tuple[bool, str]:
    """Verify Twitter credentials are still valid."""
    if not is_configured():
        return False, "Not configured"
    try:
        client = tweepy.Client(
            consumer_key=config.TWITTER_API_KEY,
            consumer_secret=config.TWITTER_API_SECRET,
            access_token=config.TWITTER_ACCESS_TOKEN,
            access_token_secret=config.TWITTER_ACCESS_SECRET,
        )
        me = client.get_me()
        if me.data:
            return True, f"Authenticated as @{me.data.username}"
        return False, "Could not verify identity"
    except tweepy.errors.Unauthorized:
        return False, "EXPIRED/INVALID: Twitter credentials are unauthorized"
    except Exception as exc:
        return False, f"Validation error: {exc}"


def publish(article: Article) -> bool:
    """Post an article to Twitter/X with retry and rate-limit awareness."""
    if not is_configured():
        logger.warning("Twitter not configured, skipping")
        return False

    allowed, reason = can_post("twitter")
    if not allowed:
        logger.info("Twitter rate limit: %s", reason)
        return False

    tweet_text = format_twitter(article)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client = tweepy.Client(
                consumer_key=config.TWITTER_API_KEY,
                consumer_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_token_secret=config.TWITTER_ACCESS_SECRET,
            )
            client.create_tweet(text=tweet_text)
            record_post("twitter")
            logger.info("Successfully posted to Twitter: %s", article.title)
            return True

        except tweepy.errors.TooManyRequests:
            wait = 60 * (2 ** attempt)
            logger.warning("Twitter rate limited, waiting %ds (attempt %d/%d)", wait, attempt, MAX_RETRIES)
            time.sleep(wait)

        except tweepy.errors.Forbidden as exc:
            logger.error("Twitter forbidden (possible duplicate or policy violation): %s", exc)
            return False

        except tweepy.errors.Unauthorized:
            logger.error("Twitter credentials expired or revoked")
            return False

        except Exception:
            if attempt == MAX_RETRIES:
                logger.exception("Failed to post to Twitter after %d attempts", MAX_RETRIES)
                return False
            wait = 30 * (2 ** attempt)
            logger.warning("Twitter error, retrying in %ds (attempt %d/%d)", wait, attempt, MAX_RETRIES)
            time.sleep(wait)

    return False
