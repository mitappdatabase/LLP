"""Uploads API Routes - File Management"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from app.core.config import settings

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    allowed = settings.ALLOWED_EXTENSIONS
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in allowed:
        raise HTTPException(400, f"File type not allowed. Allowed: {allowed}")
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(settings.UPLOAD_DIR, file.filename)
    
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"filename": file.filename, "url": f"/uploads/{file.filename}"}

@router.get("/{filename}")
async def get_file(filename: str):
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(404, "File not found")
    return FileResponse(filepath)
