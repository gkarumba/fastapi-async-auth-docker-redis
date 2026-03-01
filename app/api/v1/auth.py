import pdb

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import SessionLocal
from app.schemas.user import RefreshToken, UserCreate, UserLogin, UserRead, Token
from app.services.auth_service import AuthService
from app.repositories.user_repo import UserRepository
from app.core.jwt import decode_access_token, is_token_revoked

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await UserRepository.get_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    return await UserRepository.create(db, user)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # pdb.set_trace()
    auth_user = await AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token = AuthService.generate_token(auth_user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: RefreshToken, db: AsyncSession = Depends(get_db)):
    payload = decode_access_token(refresh_token.refresh_token)
    # pdb.set_trace()
    if not payload or refresh_token.type != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = await UserRepository.get_by_email(db, payload.get("email"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if await is_token_revoked(refresh_token.refresh_token):
        raise HTTPException(status_code=401, detail="Token revoked")
    new_access = AuthService.generate_token(user, token_type="access")
    return {"access_token": new_access, "token_type": "bearer"}