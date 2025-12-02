from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from services.ai_service import analyze_image
from sqlalchemy.orm import Session
from database.connection import get_db
from services.db_service import save_analysis_result
from services.s3_service import upload_to_s3
from routes.auth import get_current_user
from models.user import User
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Require authentication
):
    print(f"Upload request from user: {current_user.username} (ID: {current_user.id})")
    try:
        # Save uploaded image temporarily
        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        
        # Upload to S3 first (before cleaning up temp file)
        image_url = upload_to_s3(temp_path)

        # Run AWS Rekognition analysis
        result = analyze_image(temp_path)

        # Clean up
        os.remove(temp_path)

        # Save to DB with user_id
        save_analysis_result(
            db=db,
            status=result.get("status", "success"),
            labels=result.get("labels", []),
            user_id=current_user.id,
            image_url=image_url
        )

        # If Rekognition returned an error
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        labels = result.get("labels", [])

        # === SAVE TO POSTGRESQL ===
        # Choose a name: first label or "Unknown"
        name = labels[0] if labels else "Unknown"
        # === Return response to frontend ===
        return {"status": "success", "labels": labels}
        # return {"status": "success", "labels": result["labels"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload or analysis failed: {str(e)}")