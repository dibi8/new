"""LinkedIn publisher using REST API v2 with anti-ban protections."""

import logging
import time

import requests

from .. import config
from ..scraper import Article
from ..content import format_linkedin
from ..safety import can_post, record_post

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def is_configured() -> bool:
    return bool(config.LINKEDIN_ACCESS_TOKEN)


def validate_credentials() -> tuple[bool, str]:
    """Verify LinkedIn token is still valid (tokens expire in 60 days)."""
    if not is_configured():
        return False, "Not configured"
    try:
        headers = {
            "Authorization": f"Bearer {config.LINKEDIN_ACCESS_TOKEN}",
        }
        resp = requests.get(
            "https://api.linkedin.com/v2/userinfo",
            headers=headers,
            timeout=15,
        )
        if resp.status_code == 200:
            name = resp.json().get("name", "Unknown")
            return True, f"Authenticated as: {name}"
        if resp.status_code == 401:
            return False, "EXPIRED: LinkedIn token has expired (60-day limit). Regenerate via OAuth."
        return False, f"LinkedIn API error: {resp.status_code}"
    except Exception as exc:
        return False, f"Validation error: {exc}"


def publish(article: Article) -> bool:
    """Post an article to LinkedIn with retry logic."""
    if not is_configured():
        logger.warning("LinkedIn not configured, skipping")
        return False

    allowed, reason = can_post("linkedin")
    if not allowed:
        logger.info("LinkedIn rate limit: %s", reason)
        return False

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            headers = {
                "Authorization": f"Bearer {config.LINKEDIN_ACCESS_TOKEN}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            }

            if config.LINKEDIN_ORG_ID:
                author = f"urn:li:organization:{config.LINKEDIN_ORG_ID}"
            else:
                me_resp = requests.get(
                    "https://api.linkedin.com/v2/userinfo",
                    headers=headers,
                    timeout=30,
                )
                if me_resp.status_code == 401:
                    logger.error("LinkedIn token expired")
                    return False
                me_resp.raise_for_status()
                user_id = me_resp.json().get("sub", "")
                author = f"urn:li:person:{user_id}"

            commentary = format_linkedin(article)

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

            if resp.status_code in (200, 201):
                record_post("linkedin")
                logger.info("Successfully posted to LinkedIn: %s", article.title)
                return True

            if resp.status_code == 401:
                logger.error("LinkedIn token expired")
                return False

            if resp.status_code == 429:
                wait = 60 * (2 ** attempt)
                logger.warning("LinkedIn rate limited, waiting %ds", wait)
                time.sleep(wait)
                continue

            resp.raise_for_status()

        except Exception:
            if attempt == MAX_RETRIES:
                logger.exception("Failed to post to LinkedIn after %d attempts", MAX_RETRIES)
                return False
            wait = 30 * (2 ** attempt)
            logger.warning("LinkedIn error, retrying in %ds", wait)
            time.sleep(wait)

    return False
