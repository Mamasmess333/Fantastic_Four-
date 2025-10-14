from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, analysis

app = FastAPI(title="BiteWise AI Backend")

# Allow your frontend to connect (adjust port if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development — restrict later
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
