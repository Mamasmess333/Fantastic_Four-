from fastapi import APIRouter
from services.ai_service import analyze_image

router = APIRouter(prefix="/analyze", tags=["AI Analysis"])

@router.post("")
async def analyze_existing_image(data: dict):
    # Accept both 'image_url' and 'image_path' for flexibility
    image_url = data.get("image_url") or data.get("image_path")

    if not image_url:
        return {"error": "Missing image_url or image_path"}

    # Call your AI Rekognition function
    return analyze_image(image_url)
