from app.auth.depends import get_session_user
from app.database.postgres.core import get_db
from app.openapi import generate_responses
from app.tweet.models import TweetEdit, TweetIn, TweetOut
from app.tweet.orm import Tweet
from app.tweet.service import (
    create_tweet,
    delete_tweet,
    get_tweet,
    get_tweets,
    get_tweets_from_user,
    update_tweet,
)
from app.user.errors import UserNotFound
from app.utils import create_response
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import cast

router = APIRouter(prefix="/tweets", tags=["Tweet"])


@router.post("", responses=generate_responses(input=True, auth=True, responses=[(201, TweetOut)]))
async def create_tweet_route(tweet: TweetIn, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_tweet = await create_tweet(tweet=tweet, user_id=session_user_id, db=db)
    return create_response(status_code=201, body=TweetOut.model_validate(db_tweet))


@router.get("", responses=generate_responses(input=True, auth=True, responses=[(200, list[TweetOut]), (404, None)]))
async def get_tweets_route(user_id: int | None = Query(None), session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    if user_id is None:
        db_tweets = await get_tweets(db=db)

    elif user_id == 0:
        print(session_user_id)
        db_tweets = cast(list[Tweet], await get_tweets_from_user(user_id=session_user_id, db=db))

    else:
        db_tweets = await get_tweets_from_user(user_id=user_id, db=db)
        if isinstance(db_tweets, UserNotFound):
            return create_response(status_code=404)

    return create_response(status_code=200, body=[TweetOut.model_validate(db_tweet) for db_tweet in db_tweets])


@router.get("/{tweet_id}", responses=generate_responses(input=True, auth=True, responses=[(200, TweetOut), (404, None)]))
async def get_tweet_route(tweet_id: int, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_tweet = await get_tweet(tweet_id=tweet_id, db=db)

    if not db_tweet:
        return create_response(status_code=404)

    return create_response(status_code=200, body=TweetOut.model_validate(db_tweet))


@router.patch("/{tweet_id}", responses=generate_responses(input=True, auth=True, responses=[(200, TweetOut), (404, None)]))
async def update_tweet_route(tweet_id: int, tweet: TweetEdit, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_tweet = await update_tweet(tweet_id=tweet_id, user_id=session_user_id, tweet=tweet, db=db)

    if not db_tweet:
        return create_response(status_code=404)

    return create_response(status_code=200, body=TweetOut.model_validate(db_tweet))


@router.delete("/{tweet_id}", responses=generate_responses(input=True, auth=True, responses=[(200, None), (404, None)]))
async def delete_tweet_route(tweet_id: int, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_tweed_deleted = await delete_tweet(tweet_id=tweet_id, user_id=session_user_id, db=db)

    if not db_tweed_deleted:
        return create_response(status_code=404)

    return create_response(status_code=200)
