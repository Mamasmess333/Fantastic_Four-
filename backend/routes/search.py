from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from backend.services.ai_service import analyze_image
from backend.services.search_service import recommend_from_labels, search_foods

router = APIRouter(prefix="/search", tags=["Search"])


class SearchRequest(BaseModel):
    query: str


@router.post("")
def search_products(payload: SearchRequest):
    results = search_foods(payload.query)
    response = {"count": len(results), "results": results}
    if not results:
        response["message"] = "No results found."
    return response


@router.post("/from-image")
async def search_from_image(file: UploadFile = File(...)):
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / file.filename
    try:
        contents = await file.read()
        temp_path.write_bytes(contents)
        ai_result = analyze_image(str(temp_path))
    finally:
        if temp_path.exists():
            temp_path.unlink()

    if "error" in ai_result:
        raise HTTPException(status_code=500, detail=ai_result["error"])

    recommendations = recommend_from_labels(ai_result.get("labels", []))
    response = {"labels": ai_result.get("labels", []), "results": recommendations}
    if not recommendations:
        response["message"] = "No recommendations found for this meal."
    return response

