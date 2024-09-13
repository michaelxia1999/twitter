from app.database.postgres.orm import Reaction
from app.notification.service import create_notification
from app.reaction.models import ReactionIn
from app.tweet.errors import TweetNotFound
from app.tweet.service import get_tweet
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


async def create_reaction(reaction: ReactionIn, user_id: int, db: AsyncSession) -> Reaction | TweetNotFound:
    db_tweet = await get_tweet(tweet_id=reaction.tweet_id, db=db)
    if not db_tweet:
        return TweetNotFound()

    query = (
        insert(Reaction)
        .values(user_id=user_id, tweet_id=reaction.tweet_id, bookmarked=reaction.bookmarked, liked=reaction.liked)
        .on_conflict_do_update(constraint=UniqueConstraint(Reaction.tweet_id, Reaction.user_id), set_={Reaction.bookmarked: reaction.bookmarked, Reaction.liked: reaction.liked})
        .returning(Reaction)
    )
    result = await db.execute(query)

    if reaction.liked:
        await create_notification(user_id=db_tweet.user_id, body=f"User with user id {user_id} liked your tweet", db=db)

    return result.scalars().one()
