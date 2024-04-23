from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Помощь'),
            KeyboardButton(text='Привет'),
        ],
        [
            KeyboardButton(text='Пока'),
            KeyboardButton(text='Сделать скриншот'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интересует?'
)
