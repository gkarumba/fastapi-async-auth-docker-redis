from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator
import re


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise HTTPException(status_code=400, detail='Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise HTTPException(status_code=400, detail='Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise HTTPException(status_code=400, detail='Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise HTTPException(status_code=400, detail='Password must contain at least one digit')
        if not re.search(r'[@$!%*?&]', v):
            raise HTTPException(status_code=400, detail='Password must contain at least one special character (@$!%*?&)')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshToken(BaseModel):
    refresh_token: str
    type: str = "refresh"
