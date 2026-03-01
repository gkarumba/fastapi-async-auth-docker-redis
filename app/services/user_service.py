from app.repositories.user_repo import UserRepository


class UserService:

    @staticmethod
    async def create_user(db, user_data):
        existing = await UserRepository.get_by_email(db, user_data.email)
        if existing:
            raise ValueError("User already exists")

        return await UserRepository.create(db, user_data)
