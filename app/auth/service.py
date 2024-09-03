import json
import time
from app.auth.models import UserCredentials
from app.database.redis.core import redis
from app.settings import SESSION_TIMEOUT_SECONDS
from app.user.orm import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4


async def verify_user_credentials(user_credentials: UserCredentials, db: AsyncSession) -> int | None:
    query = select(User).where(User.username == user_credentials.username, User.password == user_credentials.password)
    result = await db.execute(query)
    user = result.scalars().first()

    if user:
        return user.id

    return None


async def create_session(user_id: int) -> str:
    session_id = str(uuid4())
    key = f"session_id:{session_id}"
    value = {"user_id": user_id, "created_at": int(time.time())}
    await redis.set(name=key, value=json.dumps(value), ex=SESSION_TIMEOUT_SECONDS)
    return session_id


async def verify_session(session_id: str) -> int | None:
    session = await redis.get(name=f"session_id:{session_id}")

    if not session:
        return None

    session = json.loads(session)
    user_id = session["user_id"]
    created_at = session["created_at"]
    min_created_at = await redis.get(name=f"user_id:{user_id}:session_min_created_at")

    if min_created_at and int(min_created_at) > created_at:
        return None

    return user_id


async def invalidate_session(session_id: str) -> bool:
    user_id = await verify_session(session_id=session_id)

    if not user_id:
        return False

    session_deleted = await redis.delete(f"session_id:{session_id}")
    return True if session_deleted else False


async def invalidate_all_sessions(user_id: int):
    min_created_at = int(time.time())

    # This invalidates all sessions created before this time, use case: user changes passowrd
    await redis.set(name=f"user_id:{user_id}:session_min_created_at", value=str(min_created_at), ex=SESSION_TIMEOUT_SECONDS)
