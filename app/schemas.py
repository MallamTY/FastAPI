from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint
from datetime import datetime
from typing import List, Optional, Annotated



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase): 
    id: int
    created_at: datetime
    poster_id: int
    poster: "User"
    class Config:
        orm_mode = True


class DirectPostVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

# The clean envelope container
class CustomPostEnvelopeList(BaseModel):
    message: str
    data: List[DirectPostVote]

    class Config:
        from_attributes = True

class CustomPostEnvelope(BaseModel):
    message: str
    data: DirectPostVote

    class Config:
        from_attributes = True


class PostResponseEnvelope(BaseModel):
    message: str
    data: Post

    class Config:
        orm_mode = True

class PostResponseEnvelopeList(BaseModel):
    message: str
    data: List[Post]

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserResponseEnvelope(BaseModel):
    message: str
    data: User

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class UserLoginResponse(Token):
    message: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]