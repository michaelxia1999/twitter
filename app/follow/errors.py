from app.errors import Error
from typing import Any


class SelfFollow(Error):
    location: str | None = None
    value: Any = None
    detail: str = "You can't follow yourself"
