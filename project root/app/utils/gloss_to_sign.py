# app/utils/gloss_to_sign.py
"""
Map gloss words to animation clip names (2D Lottie or file names).
Expand mapping with the animations you have in frontend/src/anims/.
"""
from typing import List, Dict

# Example mapping: gloss word (uppercase) -> animation file (without extension)
GLOSS_TO_ANIM = {
    "HELLO": "hello_wave",
    "HI": "hello_wave",
    "THANK": "thank_you",
    "THANKS": "thank_you",
    "YOU": "you_sign",
    "HOW": "how_sign",
    "ARE": "are_sign",
    "GOOD": "good_sign",
    "MORNING": "morning_sign",
    # add more mappings as you prepare anims
}

def gloss_to_sequence(gloss_text: str) -> List[Dict]:
    if not gloss_text:
        return []
    words = []
    # naive split — later improve by tokenizing punctuation
    for token in gloss_text.replace("\n", " ").split():
        w = token.strip().upper()
        if not w:
            continue
        anim = GLOSS_TO_ANIM.get(w, "idle")  # fallback to idle if not found
        # default duration (seconds), adjust as necessary
        words.append({"word": token, "animation": anim, "duration": 1.0})
    return words
