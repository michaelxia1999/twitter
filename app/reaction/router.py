from app.auth.depends import get_session_user
from app.database.postgres.core import get_db
from app.openapi import generate_responses
from app.reaction.models import ReactionIn, ReactionOut
from app.reaction.service import create_reaction
from app.tweet.errors import TweetNotFound
from app.utils import create_response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/reactions", tags=["Reaction"])


@router.post("", responses=generate_responses(input=True, auth=True, responses=[(201, ReactionOut), (404, None)]))
async def create_reaction_route(reaction: ReactionIn, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_reaction = await create_reaction(reaction=reaction, user_id=session_user_id, db=db)

    if isinstance(db_reaction, TweetNotFound):
        return create_response(status_code=404)

    return create_response(status_code=201, body=ReactionOut.model_validate(db_reaction))
