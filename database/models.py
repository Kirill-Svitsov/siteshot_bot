from sqlalchemy import String, DateTime, func, Integer, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class User(Base):
    """Таблица пользователей"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    def __repr__(self):
        return f"User: username = {self.username}, first_name = {self.first_name}"


class Screenshot(Base):
    """Таблица скриншотов"""
    __tablename__ = 'screenshots'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    url = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"<Screenshot(id={self.id}, user_id={self.user_id}, url='{self.url}')>"


class UserLog(Base):
    __tablename__ = 'user_logs'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = mapped_column(Text, nullable=False)  # Сообщение лога

    def __repr__(self):
        return f"<UserLog(id={self.id}, user_id={self.user_id})>"
