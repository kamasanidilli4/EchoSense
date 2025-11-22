# app/utils/preprocess.py
import re

def clean_text(text: str) -> str:
    # remove multiple spaces, line breaks, punctuation you don't want
    t = text.strip()
    t = re.sub(r"\s+", " ", t)
    return t
