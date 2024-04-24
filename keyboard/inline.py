from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

git_btn = InlineKeyboardButton(
    text='🤺 GIT проекта!',
    url='https://github.com/Kirill-Svitsov/siteshot_bot'
)
row = [git_btn]
rows = [row]
git = InlineKeyboardMarkup(inline_keyboard=rows)
more_btn = InlineKeyboardButton(
    text='Подробнее',
    callback_data='more'
)
more_row = [more_btn]
callback_rows = [more_row]
more = InlineKeyboardMarkup(inline_keyboard=callback_rows)