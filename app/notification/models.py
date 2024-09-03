from app.models import Model
from datetime import datetime


class NotificationOut(Model):
    id: int
    user_id: int
    body: str
    read: bool
    created_at: datetime
