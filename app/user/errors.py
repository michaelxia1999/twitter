from app.errors import Error
from typing import Any


class UsernameExist(Error):
    location: str | None = "username"
    value: Any
    detail: str = "Username already exist"


class EmailExist(Error):
    location: str | None = "email"
    value: Any
    detail: str = "Email already exist"


class UserNotFound(Error):
    location: str | None = None
    value: Any = None
    detail: str = "User not found"
