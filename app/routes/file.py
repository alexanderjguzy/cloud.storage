import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter()

UPLOAD_DIR = "uploads"


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    username: str = Form(...),
    db: Session = Depends(get_db)
):
    # Find user
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create unique filename
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Save metadata to DB
    new_file = models.File(
        filename=file.filename,   # original name
        file_path=file_path,      # stored path
        owner_id=user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"message": "File uploaded successfully"}


@router.get("/files/{username}")
def get_user_files(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    files = db.query(models.File).filter(models.File.owner_id == user.id).all()

    return files


@router.get("/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(models.File).filter(models.File.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    return FileResponse(path=file.file_path, filename=file.filename)