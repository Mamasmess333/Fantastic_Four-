from fastapi import APIRouter, UploadFile, HTTPException
from services.s3_service import upload_to_s3
from services.ai_service import analyze_image

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("")
async def upload_image(file: UploadFile):
    try:
        s3_url = upload_to_s3(file)
        ai_result = analyze_image(s3_url) 
        return {
            "image_url": s3_url,
            **ai_result
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Upload or analysis failed.")
