
from app.repositories.user_repo import UserRepository
from app.core.jwt import create_access_token
from app.core.security import verify_password


class AuthService:

    @staticmethod
    async def authenticate_user(db, username: str, password: str):
        user = await UserRepository.get_by_username(db, username)
        # pdb.set_trace()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def generate_token(user, token_type="access"):
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "type": token_type
        }
        return create_access_token(token_data)
