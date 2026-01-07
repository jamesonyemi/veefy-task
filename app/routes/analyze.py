from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
from app.services.analysis import analyze_image
from app.utils.limiter import limiter

router = APIRouter()

class AnalysisRequest(BaseModel):
    image_id: str

class AnalysisResponse(BaseModel):
    image_id: str
    skin_type: str
    issues: List[str]
    confidence: float

@router.post("/analyze", response_model=AnalysisResponse)
@limiter.limit("20/minute")
async def analyze(request: Request, analysis_req: AnalysisRequest):
    result = analyze_image(analysis_req.image_id)
    return result
