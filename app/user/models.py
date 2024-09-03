from app.models import Model
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from pydantic import Field, model_validator


class UserIn(Model):
    username: str = Field(max_length=50)
    password: str = Field(max_length=50)
    email: str = Field(max_length=100)


class UserOut(Model):
    id: int
    username: str
    password: str
    email: str
    created_at: datetime


class UserEdit(Model):
    password: str | None = Field(None, max_length=50)
    email: str | None = Field(None, max_length=100)

    @model_validator(mode="before")
    def before_check(cls, values):
        if "password" in values and values["password"] is None:
            raise RequestValidationError(errors=[{"loc": ("body", "password"), "input": None, "msg": "Password cannot be null"}])

        if "email" in values and values["email"] is None:
            raise RequestValidationError(errors=[{"loc": ("body", "email"), "input": None, "msg": "Email cannot be null"}])
        return values
