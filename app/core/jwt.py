from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.config import settings

import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost")


def create_access_token(data: dict, expires_delta=None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta=None):
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


async def blacklist_token(token: str):
    payload = decode_access_token(token)
    if payload:
        exp = payload.get("exp", 0)
        ttl = max(exp - int(datetime.utcnow().timestamp()), 0)
        await redis_client.set(token, "revoked", ex=ttl)


async def is_token_revoked(token: str) -> bool:
    return await redis_client.exists(token)