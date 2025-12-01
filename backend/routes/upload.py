from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from services.ai_service import analyze_image
from sqlalchemy.orm import Session
from database.connection import get_db
from services.db_service import save_analysis_result
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save temporarily
    os.makedirs("temp", exist_ok=True)
    temp_path = f"temp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Run AI analysis
    result = analyze_image(temp_path)

    # Clean up
    os.remove(temp_path)

    # Save to DB
    save_analysis_result(
        db=db,
        status=result.get("status", "success"),
        labels=result.get("labels", []),
        image_url=None
    )

    return {"status": "success", "labels": result["labels"]}





# @router.post("")
# async def upload_image(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)   # <-- inject DB session
# ):
#     try:
#         # Save uploaded image temporarily
#         os.makedirs("temp", exist_ok=True)
#         temp_path = f"temp/{file.filename}"
#         with open(temp_path, "wb") as f:
#             f.write(await file.read())

#         # Run AWS Rekognition analysis
#         result = analyze_image(temp_path)

#         # Clean up
#         os.remove(temp_path)

#         # If Rekognition returned an error
#         if "error" in result:
#             raise HTTPException(status_code=500, detail=result["error"])

#         labels = result.get("labels", [])

#         # === SAVE TO POSTGRESQL ===
#         # Choose a name: first label or "Unknown"
#         name = labels[0] if labels else "Unknown"
#         print("line 37 upload.py")
#         # Save to DB using your service
#         save_analysis_result(
#             db=db,
#             name=name,
#             calories=0,           # Placeholder until your analysis provides calories
#             image_url="local-temp"  # You can replace with S3 URL later
#         )
#         print("line 45 upload.py")
#         # === Return response to frontend ===
#         return {"status": "success", "labels": labels}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Upload or analysis failed: {str(e)}")