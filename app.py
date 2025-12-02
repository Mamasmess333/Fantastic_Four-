from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, analysis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="BiteWise AI Backend")

# Allow frontend (adjust if your React/Flutter uses another port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can later replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(upload.router)
app.include_router(analysis.router)

@app.get("/")
def home():
    return {"message": "BiteWise AI Backend is running 🚀"}
