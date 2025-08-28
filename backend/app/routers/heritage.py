from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import base64
from app.services.ai_service import ai_service
from app.models.heritage import (
    HeritageAnalysisRequest, 
    HeritageAnalysisResponse,
    HeritageRecommendationsResponse,
    AnalysisType
)

router = APIRouter(prefix="/heritage", tags=["heritage"])

@router.post("/analyze", response_model=HeritageAnalysisResponse)
async def analyze_heritage(
    type: AnalysisType = Form(...),
    data: str = Form(...),
    user_id: str = Form(None)
):
    """
    Analyze a heritage site from either an image or text query
    """
    try:
        if type == AnalysisType.IMAGE:
            # Decode base64 image data
            image_data = base64.b64decode(data.split(",")[1] if "," in data else data)
            result = ai_service.analyze_heritage_image(image_data)
        else:
            # Process text query
            result = ai_service.search_heritage_info(data)
            
        return HeritageAnalysisResponse(success=True, result=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/upload-image", response_model=HeritageAnalysisResponse)
async def upload_heritage_image(file: UploadFile = File(...), user_id: str = Form(None)):
    """
    Upload and analyze a heritage image
    """
    try:
        # Read image file
        image_data = await file.read()
        result = ai_service.analyze_heritage_image(image_data)
        
        return HeritageAnalysisResponse(success=True, result=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")

@router.get("/recommendations", response_model=HeritageRecommendationsResponse)
async def get_recommendations():
    """
    Get recommended heritage sites to explore
    """
    try:
        recommendations = ai_service.get_heritage_recommendations()
        return HeritageRecommendationsResponse(sites=recommendations)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")