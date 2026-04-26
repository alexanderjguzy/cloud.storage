from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Cloud Storage API is running"}