from datetime import datetime
from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, TIMESTAMP, VARCHAR
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ORM(AsyncAttrs, DeclarativeBase):
    pass


class User(ORM):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(50))
    email: Mapped[str | None] = mapped_column(VARCHAR(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))


class Tweet(ORM):
    __tablename__ = "tweet"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    body: Mapped[str] = mapped_column(VARCHAR(length=300))
    user_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))


class Reaction(ORM):
    __tablename__ = "reaction"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey(column=Tweet.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    liked: Mapped[bool]
    bookmarked: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))

    UniqueConstraint(tweet_id, user_id)


class Notification(ORM):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    body: Mapped[str] = mapped_column(TEXT)
    read: Mapped[bool] = mapped_column(server_default=text("FALSE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))


class Message(ORM):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    body: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))


class Follow(ORM):
    __tablename__ = "follow"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    followee_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))

    UniqueConstraint(follower_id, followee_id)
    CheckConstraint(follower_id != followee_id)


class Comment(ORM):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    body: Mapped[str] = mapped_column(VARCHAR(100))
    user_id: Mapped[int] = mapped_column(ForeignKey(column=User.id, ondelete="CASCADE"))
    tweet_id: Mapped[int] = mapped_column(ForeignKey(column=Tweet.id, ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))
