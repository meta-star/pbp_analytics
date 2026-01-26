from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.analytics import AnalyticsService
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: str
    version: Optional[float] = 1.0

@router.post("/analyze")
async def analyze(
    request: AnalyzeRequest,
    session: AsyncSession = Depends(get_session)
) -> Dict[str, Any]:

    analytics_service = AnalyticsService(session)
    result = await analytics_service.analyze_url(request.url)
    return result

@router.get("/")
async def health_check():
    return {"status": "alive", "service": "PBP Analytics 2026"}
