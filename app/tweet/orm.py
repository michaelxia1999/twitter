from app.database.postgres.orm import ORM
from app.user.orm import User
from datetime import datetime
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class Tweet(ORM):
    __tablename__ = "tweet"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    body: Mapped[str] = mapped_column(VARCHAR(length=300))
    user_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))
