from app.database.postgres.orm import ORM
from app.user.orm import User
from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class Follow(ORM):
    __tablename__ = "follow"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    followee_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))

    UniqueConstraint(follower_id, followee_id)
    CheckConstraint(follower_id != followee_id)
