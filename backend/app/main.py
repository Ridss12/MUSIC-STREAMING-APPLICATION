from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.auth.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music Streamer API",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Music Streamer Backend!"
    }