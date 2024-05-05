from aiogram import types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.orm_query import orm_add_user
from utils.loger import logger


async def ensure_user_exists(
        session: AsyncSession,
        message: types.Message
) -> User:
    """Функция проверки наличия пользователя в БД"""
    # Пробуем получить пользователя из БД, если он существует
    user = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = user.scalar_one_or_none()
    # Если пользователя нет в БД, создаем запись.
    if user is None:
        data = {
            'telegram_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name or None,
            'username': message.from_user.username
        }
        await orm_add_user(session, data)
        logger.info(f'Пользователь {data["username"]} добавлен в БД.')
        user = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = user.scalar_one()
    return user
