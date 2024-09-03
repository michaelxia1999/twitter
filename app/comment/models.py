from app.models import Model
from datetime import datetime
from pydantic import Field


class CommentIn(Model):
    tweet_id: int
    body: str = Field(max_length=100)


class CommentOut(Model):
    id: int
    user_id: int
    tweet_id: int
    body: str
    created_at: datetime
