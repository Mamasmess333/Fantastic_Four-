import os
import traceback

from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.services.ai_service import analyze_image
from backend.services.db_service import save_analysis
from backend.services.nutrition_service import summarize_analysis
from backend.services.s3_service import upload_to_s3

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
async def upload_image(file: UploadFile = File(...), user_id: Optional[int] = None):
    try:
        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        try:
            s3_url = upload_to_s3(temp_path, file.filename)
        except Exception as exc:
            reason = str(exc)
            if "NoSuchBucket" in reason:
                raise HTTPException(
                    status_code=400,
                    detail="S3 bucket not found. Verify S3_BUCKET_NAME or create the bucket in AWS.",
                )
            raise HTTPException(status_code=502, detail=reason)
        result = analyze_image(temp_path)
        os.remove(temp_path)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        summary = summarize_analysis(labels=result["labels"], text=None, user_goal="health", budget=None)
        analysis_id = save_analysis(
            user_id=user_id,
            image_url=s3_url,
            foods=summary["detected_items"],
            rating=summary["rating"],
            explanation=" ".join(summary["reasons"]),
            alternative=summary["suggestion"],
            metadata={"macros": summary["macros"]},
        )

        return {
            "status": "success",
            "analysis_id": analysis_id,
            "image_url": s3_url,
            **summary,
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload or analysis failed: {str(e)}")
