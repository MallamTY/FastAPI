from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
@app.get("/")
def read_root():
    return {"message": "Testing synchronization for development!!!!!!!!!!!!!!!!! sort off stuff goes here somehow"}

app.include_router(posts.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(votes.router, prefix="/api/v1")
