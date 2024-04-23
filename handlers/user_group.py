from string import punctuation

from aiogram import Bot, types, Router, F
from aiogram.filters import Command

from common.restricted_words import restricted_words
from filters.chat_types import ChatTypeFilter

user_group_router = Router()
# Устанавливаем фильтрацию на роутер для хэндлеров групповых чатов
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.message(
    F.text.lower().contains('бот') | F.text.lower().contains('помог')
)
async def answer_cmd(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(
            f"{message.from_user.first_name}, соблюддайте порядок в чате!"
        )
        await message.delete()
    else:
        await message.reply(f'Привет - {message.from_user.first_name}!\n'
                            f'Вот список моих комманд: /shot')


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(
            f"{message.from_user.first_name}, соблюддайте порядок в чате!"
        )
        await message.delete()
        # await message.chat.ban(message.from_user.id)
