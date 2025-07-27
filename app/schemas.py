from pydantic import BaseModel, EmailStr
from pydantic import field_validator
from datetime import datetime, time
from typing import Optional
from pydantic import conint
from sqlalchemy.orm import attributes
#pydantic model

class postBase(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostCreate(postBase):
    pass


class UserPost(BaseModel):
    id: int
    email: EmailStr
    # created_at: datetime 
    
    class Config:  # this is used to convert the sqlalchemy model to pydantic model
        from_attributes = True


class Post(postBase):
   created_at:datetime
   owner_id: int
   owner: UserPost

   class Config:  # this is used to convert the sqlalchemy model to pydantic model
        from_attributes=True


class PostOut(Post):
    votes:int = 0
    class Config:  # this is used to convert the sqlalchemy model to pydantic model
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

class Userlogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0) 

    class Config:
        attributes = True

