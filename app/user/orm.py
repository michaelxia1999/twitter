from app.database.postgres.orm import ORM
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class User(ORM):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(50))
    email: Mapped[str | None] = mapped_column(VARCHAR(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))
