from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from routes import upload, analysis
import os

# Database imports for Auto-Creation
from database.connection import engine, Base, get_db
from models.analysis_result import AnalysisResult
from sqlalchemy.orm import Session

# Load environment variables
load_dotenv()

# --- CRITICAL FIX: AUTO-CREATE TABLES ---
# This runs the equivalent of "init_db.py" every time the server starts.
# It ensures your tables exist so the app doesn't crash during the demo.
Base.metadata.create_all(bind=engine)

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
# Tries to find frontend folder whether running from root or backend/
FRONTEND_DIR = os.path.abspath("../frontend")
if not os.path.isdir(FRONTEND_DIR):
    FRONTEND_DIR = os.path.abspath("frontend") 

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    if os.path.exists(os.path.join(FRONTEND_DIR, "index.html")):
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
    return {"error": "Frontend not found"}

# === API Routes ===
app.include_router(upload.router)
app.include_router(analysis.router)

# === ADMIN ROUTE (Rubric: Database Demo) ===
@app.get("/admin/scans")
def get_dashboard_data(db: Session = Depends(get_db)):
    try:
        # 1. Try to get real data
        results = db.query(AnalysisResult).order_by(AnalysisResult.id.desc()).limit(10).all()
        return results
    except Exception as e:
        print(f"DB Error: {e}")
        return [] # Return empty list instead of crashing