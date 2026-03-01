from app.models.user import User
from app.core.security import hash_password
from sqlalchemy import select


class UserRepository:

    @staticmethod
    async def create(db, user_data):
        user_dict = user_data.dict()
        user_dict["password_hash"] = hash_password(user_dict.pop("password"))
        user = User(**user_dict)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_by_email(db, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_id(db, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_username(db, username: str):
        result = await db.execute(select(User).where(User.name == username))
        return result.scalar_one_or_none()
