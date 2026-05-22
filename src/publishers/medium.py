"""Medium publisher using the Medium API."""

import logging

import requests

from .. import config
from ..scraper import Article

logger = logging.getLogger(__name__)


def is_configured() -> bool:
    return bool(config.MEDIUM_TOKEN)


def publish(article: Article) -> bool:
    """Post an article to Medium."""
    if not is_configured():
        logger.warning("Medium not configured, skipping")
        return False

    try:
        headers = {
            "Authorization": f"Bearer {config.MEDIUM_TOKEN}",
            "Content-Type": "application/json",
        }

        # Get user ID
        me_resp = requests.get(
            "https://api.medium.com/v1/me",
            headers=headers,
            timeout=30,
        )
        me_resp.raise_for_status()
        user_id = me_resp.json()["data"]["id"]

        hashtags = " ".join(config.DEFAULT_HASHTAGS[:3])
        # Medium supports HTML content
        content_html = f"""
<h1>{article.title}</h1>
<p>{article.description}</p>
<p><strong>Read the full guide:</strong> <a href="{article.url}">{article.url}</a></p>
<p>{hashtags}</p>
"""

        tags = article.tags[:5] if article.tags else ["AI", "OpenSource", "DevTools"]

        payload = {
            "title": article.title,
            "contentFormat": "html",
            "content": content_html,
            "canonicalUrl": article.url,
            "tags": tags,
            "publishStatus": "public",
        }

        resp = requests.post(
            f"https://api.medium.com/v1/users/{user_id}/posts",
            headers=headers,
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        logger.info("Successfully posted to Medium: %s", article.title)
        return True

    except Exception:
        logger.exception("Failed to post to Medium")
        return False
