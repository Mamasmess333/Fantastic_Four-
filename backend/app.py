from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from routes import upload, analysis, auth
from services import ai_service, db_service, s3_service
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="BiteWise AI Backend")

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Serve static frontend ===

# Path to your frontend folder
FRONTEND_DIR = os.path.abspath("../frontend")

# Make sure folder exists
if not os.path.isdir(FRONTEND_DIR):
    raise Exception(f"Frontend folder not found: {FRONTEND_DIR}")

# Serve all files (CSS, JS, images)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


# Serve the main index page
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# === API Routes ===
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(analysis.router)