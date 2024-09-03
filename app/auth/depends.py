from app.auth.service import verify_session
from app.exc.core import ApplicationError
from fastapi import Depends
from fastapi.security import APIKeyHeader

session_id_header = APIKeyHeader(name="Session-ID", auto_error=False)


async def get_session_id(session_id: str = Depends(session_id_header)):
    return session_id


async def get_session_user(session_id: str = Depends(session_id_header)) -> int:
    user_id = await verify_session(session_id=session_id)

    if not user_id:
        raise ApplicationError(status_code=401)

    return user_id
