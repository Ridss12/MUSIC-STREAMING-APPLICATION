from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.user import User
from app.auth.auth import router as auth_router
from app.routes import setting as setting_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music Streamer API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(setting_router.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to Music Streamer Backend!"
    }