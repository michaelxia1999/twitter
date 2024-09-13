from app.database.postgres.orm import Follow
from app.follow.errors import SelfFollow
from app.follow.models import FollowIn
from app.user.errors import UserNotFound
from app.user.service import get_user
from sqlalchemy import UniqueConstraint, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


async def follow_user(follower_id: int, follow: FollowIn, db: AsyncSession) -> Follow | SelfFollow | UserNotFound:
    if follower_id == follow.user_id:
        return SelfFollow()

    db_user = await get_user(user_id=follow.user_id, db=db)

    if not db_user:
        return UserNotFound()

    query = (
        insert(Follow)
        .values(follower_id=follower_id, followee_id=follow.user_id)
        .on_conflict_do_update(constraint=UniqueConstraint(Follow.follower_id, Follow.followee_id), set_={Follow.follower_id: follower_id, Follow.followee_id: follow.user_id})
        .returning(Follow)
    )
    result = await db.execute(query)
    return result.scalars().one()


async def unfollow_user(follower_id: int, follow: FollowIn, db: AsyncSession) -> bool:
    query = delete(Follow).where(Follow.follower_id == follower_id, Follow.followee_id == follow.user_id)
    result = await db.execute(query)
    user_unfollowed = result.rowcount > 0
    return user_unfollowed
