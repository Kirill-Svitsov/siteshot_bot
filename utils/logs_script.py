from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_log
from utils.loger import logger


async def logs_script(session: AsyncSession, user_id: int, log: str):
    try:
        await orm_add_log(session, user_id, log)
    except Exception as e:
        logger.error(f'Лог не удалось записать в БД,\n'
                     f'Причина: {e}')
