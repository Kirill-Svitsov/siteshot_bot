from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Кнопка со ссылкой на ГИТ
git_btn = InlineKeyboardButton(
    text='🤺 GIT проекта!',
    url='https://github.com/Kirill-Svitsov/siteshot_bot'
)
row = [git_btn]
rows = [row]
git = InlineKeyboardMarkup(inline_keyboard=rows)
# Кнопка для WHOIS сайта
more_btn = InlineKeyboardButton(
    text='Подробнее',
    callback_data='more'
)
more_row = [more_btn]
callback_rows = [more_row]
more = InlineKeyboardMarkup(inline_keyboard=callback_rows)
