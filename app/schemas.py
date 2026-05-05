from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str


class FileResponse(BaseModel):
    id: int
    filename: str

    class Config:
        from_attributes = True