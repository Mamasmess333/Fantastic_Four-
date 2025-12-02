from fastapi import APIRouter

router = APIRouter(prefix="/support", tags=["Support"])

FAQ = {
    "meal plans": "Use the Generate button after setting your goal and budget.",
    "upload": "Tap the upload area, choose a meal photo, and wait for the AI rating.",
    "notifications": "Reminders arrive via push and email once you enable them in profile.",
}


@router.get("/faq")
def list_faq():
    return [{"question": key, "answer": value} for key, value in FAQ.items()]

