from app.models import Model
from datetime import datetime


class MessageIn(Model):
    receiver_id: int
    body: str


class MessageOut(Model):
    id: int
    sender_id: int
    receiver_id: int
    body: str
    created_at: datetime
