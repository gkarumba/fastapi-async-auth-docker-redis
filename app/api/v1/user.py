from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.create_user(db, user)
