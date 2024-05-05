from sqlalchemy import String, DateTime, func, Integer, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class User(Base):
    """Таблица пользователей"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    telegram_id: Mapped[int] = mapped_column(
        Integer,
        unique=True
    )
    first_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(150),
        nullable=True
    )
    username: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    def __repr__(self):
        return (f"User: id={self.id}, username = {self.username},"
                f" first_name = {self.first_name}")


class Screenshot(Base):
    """Таблица скриншотов"""
    __tablename__ = 'screenshots'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    url: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    def __repr__(self):
        return (f"<Screenshot(id={self.id}, "
                f"user_id={self.user_id}, url='{self.url}')>")


class UserLog(Base):
    __tablename__ = 'user_logs'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    def __repr__(self):
        return f"<UserLog(id={self.id}, user_id={self.user_id})>"
