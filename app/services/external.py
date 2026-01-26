import httpx
import gzip
import json
import logging
from typing import List, Dict, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class GoogleSafeBrowsingService:
    def __init__(self):
        self.api_key = settings.SAFE_BROWSING_API_KEY
        host = "safebrowsing.googleapis.com"
        api_ver = "v4"
        lookup_path = "threatMatches:find"
        self.lookup_url = f"https://{host}/{api_ver}/{lookup_path}?key={self.api_key}"

    async def lookup(self, urls: List[str]) -> bool:
        """
        Check if any of the URLs are unsafe.
        Returns True if unsafe (threat found), False otherwise.
        """
        if not self.api_key:
            logger.warning("Google Safe Browsing API Key not set.")
            return False

        query_urls = [{"url": url} for url in urls]
        query_data = {
            "client": {
                "clientId": "Phishing Blocker Project - Analytics",
                "clientVersion": "0.2"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": query_urls
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.lookup_url, json=query_data)
                response.raise_for_status()
                data = response.json()
                # If "matches" key exists, threats were found
                return "matches" in data and len(data["matches"]) > 0
        except Exception as e:
            logger.error(f"Error checking Safe Browsing: {e}")
            return False

class PhishTankService:
    def __init__(self):
        self.username = settings.PHISHTANK_USERNAME
        self.api_key = settings.PHISHTANK_API_KEY
        self.db_url = f"http://data.phishtank.com/data/{self.api_key}/online-valid.json.gz"

    async def get_database(self) -> List[Dict]:
        """
        Download and parse the PhishTank database (gzipped JSON).
        """
        if not self.api_key:
            logger.warning("PhishTank API Key not set.")
            return []

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(self.db_url)
                response.raise_for_status()
                decompressed_data = gzip.decompress(response.content)
                return json.loads(decompressed_data)
        except Exception as e:
            logger.error(f"Error fetching PhishTank database: {e}")
            return []

safe_browsing_service = GoogleSafeBrowsingService()
phishtank_service = PhishTankService()
