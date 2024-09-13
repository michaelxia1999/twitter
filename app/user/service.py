from app.auth.service import invalidate_all_sessions
from app.database.postgres.orm import User
from app.user.errors import EmailExist, UsernameExist
from app.user.models import UserEdit, UserIn
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(user_id: int, db: AsyncSession) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    db_user = result.scalars().first()
    return db_user


async def get_user_by_username(username: str, db: AsyncSession) -> User | None:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    db_user = result.scalars().first()
    return db_user


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    db_user = result.scalars().first()
    return db_user


async def create_user(user: UserIn, db: AsyncSession) -> User | UsernameExist | EmailExist:
    if await get_user_by_username(username=user.username, db=db):
        return UsernameExist(value=user.username)

    if await get_user_by_email(email=user.email, db=db):
        return EmailExist(value=user.email)

    query = insert(User).values(**user.model_dump()).returning(User)
    result = await db.execute(query)
    db_user = result.scalars().one()

    return db_user


async def update_user(user_id: int, user: UserEdit, db: AsyncSession) -> User | EmailExist | None:
    update_values = user.model_dump(exclude_unset=True)

    if update_values:
        if "email" in update_values:
            if await get_user_by_email(email=update_values["email"], db=db):
                return EmailExist(value=user.email)

        query = update(User).where(User.id == user_id).values(**update_values).returning(User)
    else:
        query = select(User).where(User.id == user_id)

    result = await db.execute(query)

    db_user = result.scalars().first()

    if db_user:
        if user.password:
            await invalidate_all_sessions(user_id=user_id)

    return db_user


async def delete_user(user_id: int, db: AsyncSession) -> bool:
    query = delete(User).where(User.id == user_id)
    result = await db.execute(query)

    db_user_deleted = result.rowcount > 0

    if db_user_deleted:
        await invalidate_all_sessions(user_id=user_id)
        return True

    return False
