from fastapi import FastAPI
from .database import engine, Base
from . import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Cloud Storage API is running"}