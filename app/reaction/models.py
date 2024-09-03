from app.models import Model
from datetime import datetime


class ReactionIn(Model):
    tweet_id: int
    liked: bool
    bookmarked: bool


class ReactionOut(Model):
    id: int
    tweet_id: int
    user_id: int
    liked: bool
    bookmarked: bool
    created_at: datetime
