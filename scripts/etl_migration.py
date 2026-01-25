import asyncio
import logging
import os
import sys

# Add parent dir to path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import engine
from app.models import TrustList
from app.services.browser import browser_service
from app.services.recognition import recognition_service
from app.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ETL")

async def ensure_schema(session: AsyncSession):
    """
    Ensure the schema is up to date (add new columns if missing).
    """
    try:
        # Check if column exists
        # This query is MySQL specific
        result = await session.execute(text("SHOW COLUMNS FROM trustlist LIKE 'target_view_embedding'"))
        if not result.scalar():
            logger.info("Adding missing column 'target_view_embedding' to 'trustlist' table...")
            await session.execute(text("ALTER TABLE trustlist ADD COLUMN target_view_embedding JSON DEFAULT NULL"))
            await session.commit()
            logger.info("Column added.")
        else:
            logger.info("Column 'target_view_embedding' already exists.")
    except Exception as e:
        logger.error(f"Error checking/updating schema: {e}")
        # We might fail if table doesn't exist at all, but we assume it does for migration.

async def migrate():
    logger.info("Starting ETL Migration...")

    # Ensure cache directory exists
    os.makedirs(settings.CACHE_PATH, exist_ok=True)

    async with AsyncSession(engine) as session:
        # 1. Ensure Schema
        await ensure_schema(session)

        # 2. Fetch all TrustList entries
        stmt = select(TrustList)
        result = await session.execute(stmt)
        entries = result.scalars().all()

        logger.info(f"Found {len(entries)} entries in TrustList.")

        for entry in entries:
            logger.info(f"Processing {entry.url}...")

            if entry.target_view_embedding is not None:
                logger.info(f"Embedding already exists for {entry.url}. Skipping.")
                continue

            screenshot_path = os.path.join(settings.CACHE_PATH, f"etl_{entry.uuid}.png")

            try:
                # Capture
                logger.info(f"Capturing screenshot for {entry.url}")
                browser_service.capture_screenshot(entry.url, screenshot_path)

                # Compute Embedding
                logger.info(f"Computing embedding for {entry.url}")
                embedding = recognition_service.compute_embedding(screenshot_path)

                # Update Entry
                entry.target_view_embedding = embedding
                session.add(entry)
                await session.commit()
                logger.info(f"Updated {entry.url}")

            except Exception as e:
                logger.error(f"Failed to process {entry.url}: {e}")
            finally:
                if os.path.exists(screenshot_path):
                    os.remove(screenshot_path)

    logger.info("ETL Migration Completed.")

if __name__ == "__main__":
    asyncio.run(migrate())
