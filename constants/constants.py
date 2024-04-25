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
COMMAND_LIST = (f'Вот список моих комманд:\n\n'
                f'/make_shot - сделать скриншот Web страницы. Все, что мне нужно, это полный адрес.\n\n'
                f'/hello - поздороваться\n\n'
                f'/bye - попрощаться\n\n'
                f'Случайный текст, картинка, все-что угодно тоже даст ответ!')
URL_ANSWER = 'Введите пожалуйста URL в формате: https://www.example.com.'
# Ответ на сообщение не текстового типа
NON_TYPE_ANSWER = f'К сожалению на текущий момент я умею работать только с текстом'
NON_TYPE_STICKER = 'CAACAgIAAxkBAAEE63xmJrtcBhtpevidtv75QlI83TRcUgACmjQAAogW6ErexTv1TVEynzQE'
# Стикеры процесса и завершения работы
PROCESS_STICKER = 'CAACAgIAAxkBAAEE6wpmJq3d7BAGzt7XfGP4un3-rJZo6QACHhUAAqXT6UtSdby4kVVLQjQE'
DONE_STICKER = 'CAACAgIAAxkBAAEE6zFmJq9Wtsgvl9E3JhooQgpyXNHA6QACAQADdJypFpeZtNvQv9HZNAQ'
# Неожиданный ответ
EXCEPTION_ANSWER = 'Что-то пошло не по плану'
# Ограничение размера скриншота
MAX_SIZE_PICTURE = 1900
# Директория для сохранения скриншотов
SCREENSHOTS_DIR = 'screenshots'
# Директория для сохранения логов
LOGS_DIR = 'logs'
# Валидные ответы response.status_code
VALID_STATUS_CODES = [200, 201, 202, 203, 204, 205, 206, 300, 301, 302, 303, 304, 305, 306, 307, 308]
# Headers для request get запроса
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}
# Переменные для тестов
TEST_USER_ID = 123
OK_STATUS_CODE = 200
NOT_FOUND_STATUS_CODE = 404
