import shutil
import uuid
import os
from fastapi import UploadFile, HTTPException
from app.utils.validators import MAX_FILE_SIZE_MB

UPLOAD_DIR = "uploads"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:
    # Generate unique ID
    image_id = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{image_id}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        # Save file appropriately
        # Ideally, we should read in chunks to avoid memory issues and re-check size
        size = 0
        limit = MAX_FILE_SIZE_MB * 1024 * 1024
        
        with open(file_path, "wb") as buffer:
            while content := await file.read(1024 * 1024): # Read 1MB chunks
                size += len(content)
                if size > limit:
                     # Clean up partial file
                    buffer.close()
                    os.remove(file_path)
                    raise HTTPException(status_code=400, detail="File too large (exceeded limit during upload)")
                buffer.write(content)
                
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        # Clean up if save failed
        if os.path.exists(file_path):
             os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    return image_id
