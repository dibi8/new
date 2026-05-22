"""Medium publisher using the Medium API with anti-ban protections."""

import logging
import time

import requests

from .. import config
from ..scraper import Article
from ..content import format_medium_html
from ..safety import can_post, record_post

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


def is_configured() -> bool:
    return bool(config.MEDIUM_TOKEN)


def validate_credentials() -> tuple[bool, str]:
    """Verify Medium integration token is still valid."""
    if not is_configured():
        return False, "Not configured"
    try:
        headers = {"Authorization": f"Bearer {config.MEDIUM_TOKEN}"}
        resp = requests.get("https://api.medium.com/v1/me", headers=headers, timeout=15)
        if resp.status_code == 200:
            name = resp.json().get("data", {}).get("name", "Unknown")
            return True, f"Authenticated as: {name}"
        if resp.status_code == 401:
            return False, "EXPIRED/INVALID: Medium token is invalid"
        return False, f"Medium API error: {resp.status_code}"
    except Exception as exc:
        return False, f"Validation error: {exc}"


def publish(article: Article) -> bool:
    """Post an article to Medium with retry logic."""
    if not is_configured():
        logger.warning("Medium not configured, skipping")
        return False

    allowed, reason = can_post("medium")
    if not allowed:
        logger.info("Medium rate limit: %s", reason)
        return False

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            headers = {
                "Authorization": f"Bearer {config.MEDIUM_TOKEN}",
                "Content-Type": "application/json",
            }

            me_resp = requests.get(
                "https://api.medium.com/v1/me",
                headers=headers,
                timeout=30,
            )
            if me_resp.status_code == 401:
                logger.error("Medium token expired or invalid")
                return False
            me_resp.raise_for_status()
            user_id = me_resp.json()["data"]["id"]

            content_html = format_medium_html(article)
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

            if resp.status_code in (200, 201):
                record_post("medium")
                logger.info("Successfully posted to Medium: %s", article.title)
                return True

            if resp.status_code == 429:
                wait = 120 * (2 ** attempt)
                logger.warning("Medium rate limited, waiting %ds", wait)
                time.sleep(wait)
                continue

            resp.raise_for_status()

        except Exception:
            if attempt == MAX_RETRIES:
                logger.exception("Failed to post to Medium after %d attempts", MAX_RETRIES)
                return False
            wait = 60 * (2 ** attempt)
            logger.warning("Medium error, retrying in %ds", wait)
            time.sleep(wait)

    return False
