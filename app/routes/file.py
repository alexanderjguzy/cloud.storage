import os
from fastapi import APIRouter, UploadFile, File, Depends, Form
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
        return {"error": "User not found"}

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Save to database
    new_file = models.File(
        filename=file.filename,
        file_path=file_path,
        owner_id=user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"message": "File uploaded successfully"}