# app/utils/whisper_stt.py
import os
from dotenv import load_dotenv
load_dotenv()

import whisper

_model_cache = {}

def get_model(name="small"):
    if name not in _model_cache:
        _model_cache[name] = whisper.load_model(name)
    return _model_cache[name]

def speech_to_text(audio_path, model_name="small"):
    """
    Returns transcription string.
    """
    model = get_model(model_name)
    # use fp16=True if GPU available and model supports it
    result = model.transcribe(audio_path, fp16=False)
    return result.get("text", "")
