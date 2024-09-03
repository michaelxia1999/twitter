from app.tweet.models import TweetEdit, TweetIn
from app.tweet.orm import Tweet
from app.user.errors import UserNotFound
from app.user.service import get_user
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def create_tweet(tweet: TweetIn, user_id: int, db: AsyncSession) -> Tweet:
    query = insert(Tweet).values(body=tweet.body, user_id=user_id).returning(Tweet)
    result = await db.execute(query)
    db_tweet = result.scalars().one()
    return db_tweet


async def get_tweet(tweet_id: int, db: AsyncSession) -> Tweet | None:
    query = select(Tweet).where(Tweet.id == tweet_id)
    result = await db.execute(query)
    db_tweet = result.scalars().first()
    return db_tweet


async def get_tweets(db: AsyncSession) -> list[Tweet]:
    query = select(Tweet)
    result = await db.execute(query)
    db_tweet = result.scalars().all()
    return list(db_tweet)


async def get_tweets_from_user(user_id: int, db: AsyncSession) -> list[Tweet] | UserNotFound:
    db_user = await get_user(user_id=user_id, db=db)

    if not db_user:
        return UserNotFound()

    query = select(Tweet).where(Tweet.user_id == user_id)
    result = await db.execute(query)
    db_tweets = result.scalars().all()
    return list(db_tweets)


async def update_tweet(tweet_id: int, user_id: int, tweet: TweetEdit, db: AsyncSession) -> Tweet | None:
    update_values = tweet.model_dump(exclude_unset=True)

    if update_values:
        query = update(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user_id).values(**update_values).returning(Tweet)
    else:
        query = select(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user_id)

    result = await db.execute(query)
    db_tweet = result.scalars().first()
    return db_tweet


async def delete_tweet(tweet_id: int, user_id: int, db: AsyncSession) -> bool:
    query = delete(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user_id)
    result = await db.execute(query)
    db_tweet_deleted = result.rowcount > 0
    return db_tweet_deleted
