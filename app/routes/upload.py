from fastapi import APIRouter, UploadFile, File, Depends, Request
from app.utils.validators import validate_file
from app.services.storage import save_upload_file
from pydantic import BaseModel
from app.utils.limiter import limiter

router = APIRouter()

class UploadResponse(BaseModel):
    image_id: str

@router.post("/upload", response_model=UploadResponse)
@limiter.limit("5/minute")
async def upload_image(request: Request, file: UploadFile = File(...)):
    await validate_file(file)
    image_id = await save_upload_file(file)
    return {"image_id": image_id}
