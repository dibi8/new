"""LinkedIn publisher using REST API v2."""

import logging

import requests

from .. import config
from ..scraper import Article

logger = logging.getLogger(__name__)


def is_configured() -> bool:
    return bool(config.LINKEDIN_ACCESS_TOKEN)


def publish(article: Article) -> bool:
    """Post an article to LinkedIn (personal or organization page)."""
    if not is_configured():
        logger.warning("LinkedIn not configured, skipping")
        return False

    try:
        headers = {
            "Authorization": f"Bearer {config.LINKEDIN_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

        # Determine author URN
        if config.LINKEDIN_ORG_ID:
            author = f"urn:li:organization:{config.LINKEDIN_ORG_ID}"
        else:
            # Get user profile to use as author
            me_resp = requests.get(
                "https://api.linkedin.com/v2/userinfo",
                headers=headers,
                timeout=30,
            )
            me_resp.raise_for_status()
            user_id = me_resp.json().get("sub", "")
            author = f"urn:li:person:{user_id}"

        hashtags = " ".join(config.DEFAULT_HASHTAGS[:3])
        commentary = f"{article.title}\n\n{article.description[:400]}\n\n{hashtags}"

        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": commentary},
                    "shareMediaCategory": "ARTICLE",
                    "media": [{
                        "status": "READY",
                        "originalUrl": article.url,
                        "title": {"text": article.title},
                        "description": {"text": article.description[:200]},
                    }],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        resp = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers,
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        logger.info("Successfully posted to LinkedIn: %s", article.title)
        return True

    except Exception:
        logger.exception("Failed to post to LinkedIn")
        return False
