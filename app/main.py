from fastapi import FastAPI
from app.api import upload

app = FastAPI()

app.include_router(upload.router, prefix="/upload", tags=["Upload"])

@app.get("/")
def home():
    return {"message": "Server is running"}
