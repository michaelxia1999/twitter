from app.auth.depends import get_session_id
from app.auth.models import Session, UserCredentials
from app.auth.service import create_session, invalidate_session, verify_user_credentials
from app.database.postgres.core import get_db
from app.openapi import generate_responses
from app.utils import create_response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-in", responses=generate_responses(input=True, auth=True, responses=[(201, Session)]))
async def sign_in_route(user_credentials: UserCredentials, db: AsyncSession = Depends(get_db)):
    user_id = await verify_user_credentials(user_credentials=user_credentials, db=db)

    if not user_id:
        return create_response(status_code=401)

    session_id = await create_session(user_id=user_id)
    return create_response(status_code=201, body=Session(id=session_id))


@router.post("/sign-out", responses=generate_responses(input=True, auth=True, responses=[(200, None)]))
async def sign_out_route(session_id: str = Depends(get_session_id)):
    session_invalidated = await invalidate_session(session_id=session_id)

    if not session_invalidated:
        return create_response(status_code=401)

    return create_response(status_code=200)
