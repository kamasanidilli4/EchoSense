# app/main.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routes.youtube_route import router as youtube_router

app = FastAPI(title="EchoSense+ Backend", version="1.0")

# CORS (allow local frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(youtube_router, prefix="/youtube", tags=["youtube"])

# Ensure folders exist
os.makedirs("downloads", exist_ok=True)
os.makedirs("uploads/audio", exist_ok=True)

# Serve downloads folder so frontend can access video/audio files
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

@app.get("/")
async def root():
    return {"message": "EchoSense+ Backend running"}
