from app.database.postgres.orm import ORM
from app.tweet.orm import Tweet
from app.user.orm import User
from datetime import datetime
from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class Reaction(ORM):
    __tablename__ = "reaction"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey(column=Tweet.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    liked: Mapped[bool]
    bookmarked: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))

    UniqueConstraint(tweet_id, user_id)
