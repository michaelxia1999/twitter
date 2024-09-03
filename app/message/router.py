from app.auth.depends import get_session_user
from app.database.postgres.core import get_db
from app.errors import Error
from app.message.errors import SameRecipient
from app.message.models import MessageIn, MessageOut
from app.message.service import get_message_history, send_message
from app.openapi import generate_responses
from app.user.errors import UserNotFound
from app.utils import create_response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/messages", tags=["Message"])


@router.post("", responses=generate_responses(input=True, auth=True, responses=[(201, MessageOut), (400, Error), (404, None)]))
async def send_message_route(message: MessageIn, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_message = await send_message(sender_id=session_user_id, message=message, db=db)

    if isinstance(db_message, UserNotFound):
        return create_response(status_code=404)

    if isinstance(db_message, SameRecipient):
        return create_response(status_code=400, body=SameRecipient.model_validate(db_message))

    return create_response(status_code=201, body=MessageOut.model_validate(db_message))


@router.get("", responses=generate_responses(input=True, auth=True, responses=[(200, list[MessageOut])]))
async def get_message_history_route(user_id: int, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_messages = await get_message_history(user1_id=user_id, user2_id=session_user_id, db=db)

    return create_response(status_code=200, body=[MessageOut.model_validate(db_message) for db_message in db_messages])
