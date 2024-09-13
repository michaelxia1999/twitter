from app.comment.models import CommentIn
from app.database.postgres.orm import Comment
from app.tweet.errors import TweetNotFound
from app.tweet.service import get_tweet
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_comment(comment: CommentIn, user_id: int, db: AsyncSession) -> Comment | TweetNotFound:
    db_tweet = await get_tweet(tweet_id=comment.tweet_id, db=db)

    if not db_tweet:
        return TweetNotFound()

    query = insert(Comment).values(body=comment.body, user_id=user_id, tweet_id=comment.tweet_id).returning(Comment)
    result = await db.execute(query)
    db_comment = result.scalars().one()
    return db_comment


async def get_comment(comment_id: int, db: AsyncSession) -> Comment | None:
    query = select(Comment).where(Comment.id == comment_id)
    result = await db.execute(query)
    db_comment = result.scalars().first()
    return db_comment


async def get_comments_from_tweet(tweet_id: int, db: AsyncSession) -> list[Comment] | TweetNotFound:
    db_tweet = await get_tweet(tweet_id=tweet_id, db=db)

    if not db_tweet:
        return TweetNotFound()

    query = select(Comment).where(Comment.tweet_id == tweet_id)
    result = await db.execute(query)
    db_comments = result.scalars().all()
    return list(db_comments)


async def delete_comment(comment_id: int, user_id: int, db: AsyncSession) -> bool:
    query = delete(Comment).where(Comment.id == comment_id, Comment.user_id == user_id)
    result = await db.execute(query)
    db_comment_deleted = result.rowcount > 0
    return db_comment_deleted
