from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Screenshot
from utils.loger import logger


async def orm_add_user(session: AsyncSession, data: dict):
    telegram_id = int(data['telegram_id'])
    # Проверяем, существует ли пользователь с таким telegram_id
    existing_user = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = existing_user.scalar_one_or_none()

    if user is None:
        # Если пользователь не существует, то добавляем его в базу данных
        obj = User(
            telegram_id=telegram_id,
            first_name=data['first_name'],
            last_name=data['last_name'] or None,
            username=data['username']
        )
        session.add(obj)
        await session.commit()
    else:
        logger.info(f'Пользователь {data["username"]} уже есть в БД.')


async def orm_add_screenshot(session: AsyncSession, data: dict):
    """Функция добавления скриншота в БД"""
    obj = Screenshot(
        user_id=data['user_id'],
        url=data['screenshot_path']
    )
    print(f'data["user_id"] = {data['user_id']}, тип {type(data['user_id'])}\n'
          f'data["screenshot_path"] = {data['screenshot_path']}, тип {type(data['screenshot_path'])} ')
    session.add(obj)
    await session.commit()
