from app.auth.service import verify_session
from app.exc.core import ApplicationError
from fastapi import Depends
from fastapi.security import APIKeyHeader

# Use cookie instead in production, I'm using header to pass in session id because openapi doesnt allow client(/docs) to pass in cookie
session_id_header = APIKeyHeader(name="Session-ID", auto_error=False)


async def get_session_id(session_id: str = Depends(session_id_header)):
    return session_id


async def get_session_user(session_id: str = Depends(session_id_header)) -> int:
    user_id = await verify_session(session_id=session_id)

    if not user_id:
        raise ApplicationError(status_code=401)

    return user_id
