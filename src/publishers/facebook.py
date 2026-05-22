"""Facebook Page publisher using Graph API."""

import logging

import requests

from .. import config
from ..scraper import Article

logger = logging.getLogger(__name__)


def is_configured() -> bool:
    return all([config.FACEBOOK_PAGE_ID, config.FACEBOOK_ACCESS_TOKEN])


def publish(article: Article) -> bool:
    """Post an article to a Facebook Page."""
    if not is_configured():
        logger.warning("Facebook not configured, skipping")
        return False

    try:
        url = f"https://graph.facebook.com/v19.0/{config.FACEBOOK_PAGE_ID}/feed"

        hashtags = " ".join(config.DEFAULT_HASHTAGS[:3])
        message = f"{article.title}\n\n{article.description[:300]}\n\n{hashtags}"

        payload = {
            "message": message,
            "link": article.url,
            "access_token": config.FACEBOOK_ACCESS_TOKEN,
        }

        resp = requests.post(url, data=payload, timeout=30)
        resp.raise_for_status()
        logger.info("Successfully posted to Facebook: %s", article.title)
        return True

    except Exception:
        logger.exception("Failed to post to Facebook")
        return False
