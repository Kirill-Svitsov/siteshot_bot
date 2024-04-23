# Список допустимых обновлений
ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']
# Приветственные слова
GREETINGS_WORDS = (
    'привет',
    'здравствуй',
    'хай',
    'хэллоу',
    'hi',
    'hello'
)
# Прощальные слова
FAREWELL_WORDS = (
    'пока',
    'пакеда',
    'до свидания',
    'всего хорошего',
    'бай',
    'bye'
)
# Приветственный ответ
GREETING_ANSWER = ' - здравствуй!\nЧтобы узнать какие команды у меня есть, нажми /help'
HASBIK_HELLO = 'CAACAgIAAxkBAAEE6wRmJq0v6wiiJw980QeqnPsAAX0HJuIAAtcYAAJuJuFLBWMtwpjr_Ks0BA'
# Прощание
BYE_ANSWER = f'До свиданий, дорогой '
BYE_STICKER = 'CAACAgIAAxkBAAEE6xZmJq7g6za9IijujoZLfFp6deh3GwACNBIAAhKD-Uv6vzFHb73KAjQE'
# Ответ на неизвестную команду
UNKNOWN_ANSWER = f'к сожалению у меня нет команды: '
UNKNOWN_STICKER = 'CAACAgIAAxkBAAEE6w5mJq5UrKhBRLuaYC6pz8z3eBPjNwACpQUAAiMFDQABrU3UopUKcHs0BA'
# Список команд
COMMAND_LIST = (f'Вот список моих комманд:\n'
                f'/make_shot - сделать скриншот Web страницы. Все, что мне нужно, это полный адрес.\n'
                f'/hello - поздороваться\n'
                f'/bye - попрощаться\n'
                f'Случайный текст, картинка, все-что угодно тоже даст ответ!')
URL_ANSWER = ('введи пожалуйста URL в формате: https://www.example.com\n'
              'Или нажми на /cancel, чтобы отменить операцию.')
# Ответ на сообщение не текстового типа
NON_TYPE_ANSWER = f'К сожалению на текущий момент я умею работать только с текстом'
NON_TYPE_STICKER = 'CAACAgIAAxkBAAEE63xmJrtcBhtpevidtv75QlI83TRcUgACmjQAAogW6ErexTv1TVEynzQE'
# Стикеры процесса и завершения работы
PROCESS_STICKER = 'CAACAgIAAxkBAAEE6wpmJq3d7BAGzt7XfGP4un3-rJZo6QACHhUAAqXT6UtSdby4kVVLQjQE'
DONE_STICKER = 'CAACAgIAAxkBAAEE6zFmJq9Wtsgvl9E3JhooQgpyXNHA6QACAQADdJypFpeZtNvQv9HZNAQ'
# Неожиданный ответ
EXCEPTION_ANSWER = 'Что-то пошло не по плану'
MAX_SIZE_PICTURE = 1900
