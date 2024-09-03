from app.database.postgres.orm import ORM
from app.user.orm import User
from datetime import datetime
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class Message(ORM):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    body: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))
