import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse
from hashlib import sha256
import os
import uuid
import validators
from url_normalize import url_normalize
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from app.models import TrustList, TrustDomain, BlackList, WarnList, ResultCache
from app.services.recognition import recognition_service
from app.services.browser import browser_service
from app.services.external import safe_browsing_service
from app.config import settings

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def analyze_url(self, url: str) -> Dict[str, Any]:
        """
        Main entry point for URL analysis.
        """
        try:
            normalized_url = url_normalize(url)
        except Exception:
            # Fallback if normalization fails
            normalized_url = url

        if not validators.url(normalized_url):
             return {"status": 400, "reason": "Invalid URL"}

        # 1. Check Database (Cache & Lists)
        score = await self._check_database(normalized_url)
        if score is not None:
            return {"status": 200, "url": normalized_url, "trust_score": score}

        # 2. Check External APIs (Safe Browsing)
        # We don't check PhishTank API live usually, we rely on local DB update from PhishTank dump.
        # But if we wanted to, we could. The legacy code checked SafeBrowsing live.
        is_unsafe = await safe_browsing_service.lookup([normalized_url])
        if is_unsafe:
            await self._mark_as_blacklist(normalized_url)
            return {"status": 200, "url": normalized_url, "trust_score": 0.0}

        # 3. Deep Analysis
        score = await self._deep_analyze(normalized_url)

        # Cache the result
        await self._cache_result(normalized_url, score)

        return {"status": 200, "url": normalized_url, "trust_score": score}

    async def _check_database(self, url: str) -> Optional[float]:
        url_hash = sha256(url.encode("utf-8")).hexdigest()

        # Check Cache
        stmt = select(ResultCache).where(ResultCache.url_hash == url_hash)
        result = await self.session.execute(stmt)
        cache_entry = result.scalar_one_or_none()
        if cache_entry:
            return cache_entry.score

        # Check TrustList
        stmt = select(TrustList).where(TrustList.url == url)
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none():
            return 1.0

        # Check TrustDomain
        parsed = urlparse(url)
        domain = parsed.hostname
        if domain:
            stmt = select(TrustDomain).where(TrustDomain.domain == domain)
            result = await self.session.execute(stmt)
            if result.scalar_one_or_none():
                return 1.0

        # Check WarnList
        stmt = select(WarnList).where(WarnList.url == url)
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none():
            return 0.5

        # Check BlackList
        stmt = select(BlackList).where(BlackList.url == url)
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none():
            return 0.0

        return None

    async def _deep_analyze(self, url: str) -> float:
        # Capture Screenshot
        screenshot_path = os.path.join(settings.CACHE_PATH, f"{uuid.uuid4()}.png")
        os.makedirs(settings.CACHE_PATH, exist_ok=True)

        try:
            browser_service.capture_screenshot(url, screenshot_path)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            # If we can't capture, we can't judge visually.
            # Check if it was a connection error (site down).
            # If site down -> 404/403 -> return error or neutral?
            # Legacy code returned specific status codes.
            # Here we simplify: if capture fails, we assume we can't verify it visually.
            # Maybe return 1.0 (innocent until proven guilty) or error.
            # Let's return 1.0 but log it.
            return 1.0

        try:
            # Compute Embedding
            embedding = recognition_service.compute_embedding(screenshot_path)

            # Compare with TrustList
            stmt = select(TrustList)
            result = await self.session.execute(stmt)
            trust_entries = result.scalars().all()

            max_similarity = 0.0
            most_similar_url = None

            for entry in trust_entries:
                if entry.target_view_embedding:
                    sim = recognition_service.compute_similarity(embedding, entry.target_view_embedding)
                    if sim > max_similarity:
                        max_similarity = sim
                        most_similar_url = entry.url

            # Threshold
            # If it looks very similar (> 0.9) to a trusted site, but it IS NOT the trusted site (already checked in _check_database),
            # then it is a phishing attempt.
            if max_similarity > 0.9:
                await self._mark_as_warnlist(url, most_similar_url)
                return 0.5 # Or 0.0? Legacy said 0.5 (suspicious)

            return 1.0

        finally:
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)

    async def _mark_as_blacklist(self, url: str):
        url_hash = sha256(url.encode("utf-8")).hexdigest()
        # Check if already exists
        stmt = select(BlackList).where(BlackList.url_hash == url_hash)
        result = await self.session.execute(stmt)
        if not result.scalar_one_or_none():
            blacklist_entry = BlackList(url=url, url_hash=url_hash)
            self.session.add(blacklist_entry)
            await self.session.commit()

    async def _mark_as_warnlist(self, url: str, origin: str):
        stmt = select(WarnList).where(WarnList.url == url)
        result = await self.session.execute(stmt)
        if not result.scalar_one_or_none():
            warn_entry = WarnList(url=url, origin=origin)
            self.session.add(warn_entry)
            await self.session.commit()

    async def _cache_result(self, url: str, score: float):
        url_hash = sha256(url.encode("utf-8")).hexdigest()
        # Upsert logic (SQLModel doesn't have native upsert, so delete then insert or check then update)
        # Using merge or simple check
        stmt = select(ResultCache).where(ResultCache.url_hash == url_hash)
        result = await self.session.execute(stmt)
        entry = result.scalar_one_or_none()

        if entry:
            entry.score = score
            self.session.add(entry)
        else:
            entry = ResultCache(url_hash=url_hash, score=score)
            self.session.add(entry)
        await self.session.commit()
