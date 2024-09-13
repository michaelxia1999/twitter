from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BIGINT, BOOLEAN, TEXT, TIMESTAMP, VARCHAR
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ORM(AsyncAttrs, DeclarativeBase):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))


class User(ORM):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(50))
    email: Mapped[str | None] = mapped_column(VARCHAR(100), unique=True)


class Tweet(ORM):
    __tablename__ = "tweet"

    body: Mapped[str] = mapped_column(VARCHAR(length=300))
    user_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))


class Reaction(ORM):
    __tablename__ = "reaction"

    tweet_id: Mapped[int] = mapped_column(ForeignKey(column=Tweet.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    liked: Mapped[bool]
    bookmarked: Mapped[bool]
    UniqueConstraint(tweet_id, user_id)


class Notification(ORM):
    __tablename__ = "notification"

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    body: Mapped[str] = mapped_column(TEXT)
    read: Mapped[bool] = mapped_column(BOOLEAN)


class Message(ORM):
    __tablename__ = "message"

    sender_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    body: Mapped[str] = mapped_column(TEXT)


class Follow(ORM):
    __tablename__ = "follow"

    follower_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    followee_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))

    UniqueConstraint(follower_id, followee_id)
    CheckConstraint(follower_id != followee_id)


class Comment(ORM):
    __tablename__ = "comment"

    body: Mapped[str] = mapped_column(VARCHAR(100))
    user_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    tweet_id: Mapped[int] = mapped_column(ForeignKey(column=Tweet.id, ondelete="CASCADE"))
