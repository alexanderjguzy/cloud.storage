import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..dependencies import get_current_user
from .. import schemas

router = APIRouter()

UPLOAD_DIR = "uploads"

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_TYPES = ["image/png", "image/jpeg", "application/pdf"]

@router.post("/upload", response_model=schemas.FileResponse)
def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find user
    user = current_user

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create unique filename
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    # read file content ONCE
    content = file.file.read()

    #  size check
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    #  type check
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    #  save file AFTER validation
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    #  save metadata to DB
    new_file = models.File(
        filename=file.filename,
        file_path=file_path,
        owner_id=user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file


@router.get("/files", response_model=list[schemas.FileResponse])
def get_user_files(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    files = db.query(models.File).filter(models.File.owner_id == current_user.id).all()
    return files

@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(models.File).filter(models.File.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # ownership check
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="File missing")

    return FileResponse(path=file.file_path, filename=file.filename)


@router.delete("/delete/{file_id}")
def delete_file(
    file_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(models.File).filter(models.File.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # ownership check
    if file.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # delete file from disk
    if os.path.exists(file.file_path):
        os.remove(file.file_path)

    # delete from DB
    db.delete(file)
    db.commit()

    return {"message": "File deleted"}












