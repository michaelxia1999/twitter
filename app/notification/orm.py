from app.database.postgres.orm import ORM
from app.user.orm import User
from datetime import datetime
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import BIGINT, ENUM, TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class Notification(ORM):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    body: Mapped[str] = mapped_column(TEXT)
    read: Mapped[bool] = mapped_column(server_default=text("FALSE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))
