from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import user
from .routes import file
from .routes import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)

app.include_router(file.router)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Cloud Storage API is running"}