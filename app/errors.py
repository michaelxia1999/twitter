from app.models import Model
from typing import Any


class Error(Model):
    location: str | None
    value: Any
    detail: str
