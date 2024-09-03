from app.errors import Error
from typing import Any


class TweetNotFound(Error):
    location: str | None = None
    value: Any = None
    detail: str = "Tweet not found"
