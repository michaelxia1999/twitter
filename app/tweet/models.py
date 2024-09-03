from app.models import Model
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from pydantic import Field, model_validator


class TweetIn(Model):
    body: str = Field(max_length=300)


class TweetOut(Model):
    id: int
    body: str
    user_id: int
    created_at: datetime


class TweetEdit(Model):
    body: str | None = Field(None, max_length=300)

    @model_validator(mode="before")
    def before_check(cls, values):
        if "body" in values and values["body"] is None:
            raise RequestValidationError(errors=[{"loc": ("body", "body"), "input": None, "msg": "Body cannot be null"}])

        return values
