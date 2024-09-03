from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class ORM(AsyncAttrs, DeclarativeBase):
    pass
