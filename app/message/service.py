from app.message.errors import SameRecipient
from app.message.models import MessageIn
from app.message.orm import Message
from app.user.errors import UserNotFound
from app.user.service import get_user
from sqlalchemy import desc, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


async def send_message(sender_id: int, message: MessageIn, db: AsyncSession) -> Message | UserNotFound | SameRecipient:
    if sender_id == message.receiver_id:
        return SameRecipient()

    db_user = await get_user(user_id=message.receiver_id, db=db)

    if not db_user:
        return UserNotFound()

    query = insert(Message).values(sender_id=sender_id, receiver_id=message.receiver_id, body=message.body).returning(Message)
    result = await db.execute(query)
    db_message = result.scalars().one()
    return db_message


async def get_message_history(user1_id: int, user2_id: int, db: AsyncSession) -> list[Message]:
    query = (
        select(Message)
        .where(or_((Message.sender_id == user1_id) & (Message.receiver_id == user2_id), (Message.sender_id == user2_id) & (Message.receiver_id == user1_id)))
        .order_by(desc(Message.created_at))
    )
    result = await db.execute(query)
    db_messages = list(result.scalars().all())

    return db_messages
