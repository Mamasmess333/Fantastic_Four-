from fastapi import APIRouter, UploadFile, File, HTTPException
from services.ai_service import analyze_image
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded image temporarily
        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Run AWS Rekognition analysis
        result = analyze_image(temp_path)

        # Clean up
        os.remove(temp_path)

        # Return the analysis result
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return {"status": "success", "labels": result["labels"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload or analysis failed: {str(e)}")
