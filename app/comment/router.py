from app.auth.depends import get_session_user
from app.comment.models import CommentIn, CommentOut
from app.comment.service import create_comment, delete_comment, get_comment, get_comments_from_tweet
from app.database.postgres.core import get_db
from app.openapi import generate_responses
from app.tweet.errors import TweetNotFound
from app.utils import create_response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/comments", tags=["Comment"])


@router.post("", responses=generate_responses(input=True, auth=True, responses=[(201, CommentOut), (404, None)]))
async def create_comment_route(comment: CommentIn, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_comment = await create_comment(comment=comment, user_id=session_user_id, db=db)

    if isinstance(db_comment, TweetNotFound):
        return create_response(status_code=404)

    return create_response(status_code=201, body=CommentOut.model_validate(db_comment))


@router.get("/{comment_id}", responses=generate_responses(input=True, auth=True, responses=[(200, CommentOut), (404, None)]))
async def get_comment_route(comment_id: int, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_comment = await get_comment(comment_id=comment_id, db=db)

    if not db_comment:
        return create_response(status_code=404)

    return create_response(status_code=200, body=CommentOut.model_validate(db_comment))


@router.delete("/{comment_id}", responses=generate_responses(input=True, auth=True, responses=[(200, None), (404, None)]))
async def delete_my_comment_route(comment_id: int, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_comment_deleted = await delete_comment(comment_id=comment_id, user_id=session_user_id, db=db)

    if not db_comment_deleted:
        return create_response(status_code=404)

    return create_response(status_code=200)


@router.get("", responses=generate_responses(input=True, auth=True, responses=[(200, list[CommentOut]), (404, None)]))
async def get_comments_from_tweet_route(tweet_id: int, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_comments = await get_comments_from_tweet(tweet_id=tweet_id, db=db)

    if isinstance(db_comments, TweetNotFound):
        return create_response(status_code=404)

    return create_response(status_code=200, body=[CommentOut.model_validate(db_comment) for db_comment in db_comments])
