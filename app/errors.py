from app.models import Model
from typing import Any


# Base class for all errors, all errors return to the client should follow this format
class Error(Model):
    location: str | None
    value: Any
    detail: str
