import random
import os
from fastapi import HTTPException

UPLOAD_DIR = "uploads"

# Mock data
SKIN_TYPES = ["Oily", "Dry", "Combination", "Normal", "Sensitive"]
ISSUES = ["Acne", "Hyper-pigmentation", "Wrinkles", "Redness", "Pores", "Dark Circles"]

def analyze_image(image_id: str) -> dict:
    # Verify file exists (simulate processing the file)
    # We search for any file starting with image_id in the uploads dir
    # because we don't know the extension without checking.
    
    file_found = False
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            if filename.startswith(image_id):
                file_found = True
                break
    
    if not file_found:
        raise HTTPException(status_code=404, detail="Image not found")

    # Simulate processing time or logic
    # Here we just return random mock data
    
    return {
        "image_id": image_id,
        "skin_type": random.choice(SKIN_TYPES),
        "issues": random.sample(ISSUES, k=random.randint(0, 3)),
        "confidence": round(random.uniform(0.70, 0.99), 2)
    }
