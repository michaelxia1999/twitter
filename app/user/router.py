from app.auth.depends import get_session_user
from app.database.postgres.core import get_db
from app.errors import Error
from app.openapi import generate_responses
from app.user.errors import EmailExist, UsernameExist
from app.user.models import UserEdit, UserIn, UserOut
from app.user.service import create_user, delete_user, get_user, update_user
from app.utils import create_response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["User"])


@router.post("", responses=generate_responses(input=True, auth=False, responses=[(201, UserOut), (409, Error)]))
async def create_user_route(user: UserIn, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(user=user, db=db)

    if isinstance(db_user, (UsernameExist, EmailExist)):
        return create_response(status_code=409, body=db_user)

    return create_response(status_code=201, body=UserOut.model_validate(db_user))


@router.get("", responses=generate_responses(input=True, auth=True, responses=[(200, UserOut)]))
async def get_user_route(session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_user = await get_user(user_id=session_user_id, db=db)

    if not db_user:
        return create_response(status_code=500)

    return create_response(status_code=200, body=UserOut.model_validate(db_user))


@router.patch("", responses=generate_responses(input=True, auth=True, responses=[(200, UserOut), (404, None), (409, Error)]))
async def update_user_route(user: UserEdit, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_user = await update_user(user_id=session_user_id, user=user, db=db)

    if not db_user:
        return create_response(status_code=404)

    if isinstance(db_user, EmailExist):
        return create_response(status_code=409, body=db_user)

    return create_response(status_code=200, body=UserOut.model_validate(db_user))


@router.delete("", responses=generate_responses(input=True, auth=True, responses=[(200, None), (404, None)]))
async def delete_user_route(session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_user_deleted = await delete_user(user_id=session_user_id, db=db)

    if not db_user_deleted:
        return create_response(status_code=404)

    return create_response(status_code=200)
