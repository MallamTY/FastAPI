from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()

@app.get("/")
def homePage():
    return {"message": "Hello World. Added something for a test"}


@app.get("/posts")
async def get_post():
    return {"message": "This is the posts endpoint"}


@app.post("/pos t/create")
async def create_post(payload: Post):
    print(payload.rating)
    return {
        "message": "Post created successfully",
        "data": payload
        }