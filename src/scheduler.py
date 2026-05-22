"""Main scheduler: pick a random unpublished article and publish to all platforms."""

import logging
import sys

from .scraper import get_unpublished_article, save_published
from .publishers import twitter, facebook, linkedin, medium, reddit

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

PLATFORMS = [
    ("twitter", twitter),
    ("facebook", facebook),
    ("linkedin", linkedin),
    ("medium", medium),
    ("reddit", reddit),
]


def run() -> None:
    """Run one publish cycle: pick article, post to all configured platforms."""
    logger.info("=== Starting publish cycle ===")

    results: dict[str, bool] = {}

    for platform_name, publisher in PLATFORMS:
        if not publisher.is_configured():
            logger.info("Skipping %s (not configured)", platform_name)
            continue

        article = get_unpublished_article(platform_name)
        if article is None:
            logger.warning("No article available for %s", platform_name)
            continue

        logger.info("Publishing to %s: %s", platform_name, article.title)
        success = publisher.publish(article)
        results[platform_name] = success

        if success:
            save_published(platform_name, article.url)
            logger.info("Published and recorded: %s -> %s", article.url, platform_name)
        else:
            logger.error("Failed to publish to %s: %s", platform_name, article.title)

    # Summary
    logger.info("=== Publish cycle complete ===")
    for platform_name, success in results.items():
        status = "OK" if success else "FAILED"
        logger.info("  %s: %s", platform_name, status)

    if not results:
        logger.info("  No platforms configured. Set up API keys to enable publishing.")

    # Exit with error code if any publication failed
    if any(not s for s in results.values()):
        sys.exit(1)


if __name__ == "__main__":
    run()
