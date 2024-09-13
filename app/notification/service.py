from app.database.postgres.orm import Notification
from app.user.errors import UserNotFound
from app.user.service import get_user
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def create_notification(user_id: int, body: str, db: AsyncSession) -> UserNotFound | Notification:
    db_user = await get_user(user_id=user_id, db=db)

    if not db_user:
        return UserNotFound()

    query = insert(Notification).values(user_id=user_id, body=body, read=False).returning(Notification)
    result = await db.execute(query)
    db_notification = result.scalars().one()
    return db_notification


async def get_notifications_from_user(user_id: int, db: AsyncSession) -> list[Notification]:
    query = select(Notification).where(Notification.user_id == user_id)
    result = await db.execute(query)
    db_notifications = result.scalars().all()
    return list(db_notifications)


async def read_notification(notification_id: int, user_id: int, db: AsyncSession) -> Notification | None:
    query = update(Notification).where(Notification.id == notification_id, Notification.user_id == user_id).values(read=True).returning(Notification)
    result = await db.execute(query)
    db_notification = result.scalars().first()

    return db_notification
