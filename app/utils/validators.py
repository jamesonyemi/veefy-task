from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE_MB = 5
ALLOWED_TYPES = ["image/jpeg", "image/png"]

async def validate_file(file: UploadFile):
    # Validate content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_TYPES)}"
        )
    
    # Validate size (checking Content-Length header first)
    # Note: This relies on the client sending the header.
    # We will also enforce it during read/save if needed, but this is a good first check.
    # For a robust implementation, we would count bytes during stream.
    if file.size and file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
         raise HTTPException(
            status_code=400, 
            detail=f"File too large. Max allowed: {MAX_FILE_SIZE_MB}MB"
        )
    
    # Alternative validaton if file.size is not populated (e.g. chunked transfer)
    # We can handle this in the storage service by limiting the read.
