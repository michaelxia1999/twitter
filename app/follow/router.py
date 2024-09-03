from app.auth.depends import get_session_user
from app.database.postgres.core import get_db
from app.follow.errors import SelfFollow
from app.follow.models import FollowIn
from app.follow.service import follow_user, unfollow_user
from app.openapi import generate_responses
from app.user.errors import UserNotFound
from app.utils import create_response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/follows", tags=["Follow"])


@router.post("", responses=generate_responses(input=True, auth=True, responses=[(200, None), (404, None)]))
async def follow_user_route(follow: FollowIn, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_follow = await follow_user(follower_id=session_user_id, follow=follow, db=db)

    if isinstance(db_follow, SelfFollow):
        return create_response(status_code=400)

    if isinstance(db_follow, UserNotFound):
        return create_response(status_code=404)

    return create_response(status_code=200)


@router.delete("", responses=generate_responses(input=True, auth=True, responses=[(200, None), (404, None)]))
async def unfollow_user_route(follow: FollowIn, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    user_unfollowed = await unfollow_user(follower_id=session_user_id, follow=follow, db=db)

    if not user_unfollowed:
        return create_response(status_code=404)

    return create_response(status_code=200)
