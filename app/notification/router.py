from app.auth.depends import get_session_user
from app.database.postgres.core import get_db
from app.notification.models import NotificationOut
from app.notification.service import get_notifications_from_user, read_notification
from app.openapi import generate_responses
from app.utils import create_response
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/notifications", tags=["Notification"])


@router.get("", responses=generate_responses(input=True, auth=True, responses=[(200, list[NotificationOut])]))
async def get_notifications_from_user_route(session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_notifications = await get_notifications_from_user(user_id=session_user_id, db=db)

    return create_response(status_code=200, body=[NotificationOut.model_validate(db_notification) for db_notification in db_notifications])


@router.get("/{notification_id}", responses=generate_responses(input=True, auth=True, responses=[(200, NotificationOut), (404, None)]))
async def read_notification_route(notification_id: int, session_user_id: int = Depends(get_session_user), db: AsyncSession = Depends(get_db)):
    db_notification = await read_notification(notification_id=notification_id, user_id=session_user_id, db=db)

    if not db_notification:
        return create_response(status_code=404)

    return create_response(status_code=200, body=NotificationOut.model_validate(db_notification))
