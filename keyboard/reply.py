from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура выбора языка
choose_language = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='English'),
            KeyboardButton(text='Русский'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Пожалуйста, выберите язык для продолжения.'
)
# Русская клавиатура
ru_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Помощь'),
            KeyboardButton(text='Привет'),
        ],
        [
            KeyboardButton(text='Пока'),
            KeyboardButton(text='Сделать скриншот'),
        ],
        [
            KeyboardButton(text='Выбрать язык'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интересует?'
)
# Английская клавиатура
en_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Help'),
            KeyboardButton(text='Hello'),
        ],
        [
            KeyboardButton(text='Bye'),
            KeyboardButton(text='Make Screen'),
        ],
        [
            KeyboardButton(text='Chose language'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='What are you interested in?'
)
lng = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Chose language'),
            KeyboardButton(text='Выбрать язык'),
        ],
    ],
    resize_keyboard=True,
)
