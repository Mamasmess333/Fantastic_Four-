from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from backend.routes import (
    analysis,
    chatbot_route,
    feedback,
    meal_plans,
    notifications,
    search,
    support,
    upload,
    users,
)
from backend.services.db_service import init_db
import os

load_dotenv()

app = FastAPI(title="BiteWise AI Backend")


@app.on_event("startup")
def _startup():
    init_db()

# === Allow frontend ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Serve frontend ===
FRONTEND_DIR = os.path.abspath("frontend")
if not os.path.isdir(FRONTEND_DIR):
    print(f"⚠️ Frontend folder not found: {FRONTEND_DIR}")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# === Routes ===
app.include_router(upload.router)
app.include_router(analysis.router)
app.include_router(users.router)
app.include_router(meal_plans.router)
app.include_router(search.router)
app.include_router(notifications.router)
app.include_router(feedback.router)
app.include_router(support.router)
app.include_router(chatbot_route.router)
