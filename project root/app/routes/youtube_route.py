# app/routes/youtube_route.py
import os
import subprocess
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.youtube_downloader import download_youtube
from app.utils.whisper_stt import speech_to_text
from app.utils.gloss_nlp import text_to_gloss
from app.utils.gloss_to_sign import gloss_to_sequence

router = APIRouter()

class YTRequest(BaseModel):
    url: str
    model: str = "small"      # whisper model name to use optionally

@router.post("/process")
async def process_youtube(req: YTRequest):
    url = req.url
    if not url:
        raise HTTPException(status_code=400, detail="No url provided")

    # unique id per request
    uid = uuid.uuid4().hex[:8]
    video_out = f"downloads/video_{uid}.mp4"
    audio_out = f"downloads/audio_{uid}.wav"

    # 1. Download video
    try:
        download_youtube(url, out=video_out)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"yt-dlp download failed: {e}")

    # 2. Extract audio (16k mono wav) with ffmpeg
    try:
        # overwrite existing if any
        cmd = [
            "ffmpeg", "-y",
            "-i", video_out,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            audio_out
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ffmpeg audio extraction failed: {e}")

    # 3. Whisper STT
    try:
        text = speech_to_text(audio_out, model_name=req.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT failed: {e}")

    # 4. Text -> Gloss (HuggingFace SignKit or other HF model)
    try:
        gloss = text_to_gloss(text)
    except Exception as e:
        gloss = ""  # continue even if gloss API fails

    # 5. Gloss -> animation sequence (mapped clips)
    sequence = gloss_to_sequence(gloss)

    # 6. Return JSON (frontend will use /downloads/video_xxx.mp4)
    return {
        "status": "ok",
        "video_url": f"/downloads/{os.path.basename(video_out)}",
        "audio_url": f"/downloads/{os.path.basename(audio_out)}",
        "transcription": text,
        "gloss": gloss,
        "sign_sequence": sequence
    }
