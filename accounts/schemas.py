
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str