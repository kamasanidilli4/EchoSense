# app/utils/gloss_nlp.py
import os
import requests
from dotenv import load_dotenv
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_GLOSS_MODEL = os.getenv("HF_GLOSS_MODEL")  # example: "your-username/english-to-ISL-gloss"

if not HF_API_KEY or not HF_GLOSS_MODEL:
    # will still allow local dev, return identity
    def text_to_gloss(text):
        return text.upper()
else:
    HF_URL = f"https://api-inference.huggingface.co/models/{HF_GLOSS_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    def text_to_gloss(text):
        payload = {"inputs": text}
        resp = requests.post(HF_URL, headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            # fallback: uppercase words
            return text.upper()
        data = resp.json()
        # model-specific: try to extract generated_text or string
        if isinstance(data, dict) and "error" in data:
            return text.upper()
        if isinstance(data, list):
            # common response: [{"generated_text": "..."}]
            first = data[0]
            return first.get("generated_text", str(first))
        if isinstance(data, str):
            return data
        return str(data)
