from fastapi import APIRouter
from services.ai_service import analyze_image

router = APIRouter(prefix="/analyze", tags=["AI Analysis"])

@router.post("")
async def analyze_existing_image(data: dict):
    image_url = data.get("image_url")
    if not image_url:
        return {"error": "Missing image_url"}
    return analyze_image(image_url)
