[![GitHub](https://img.shields.io/badge/GitHub-Kirill--Svitsov-blue)](https://github.com/Kirill-Svitsov)
# Site shot bot 
[![Telegram Badge](https://img.shields.io/badge/-siteshotbot-blue?style=flat&logo=Telegram&logoColor=white)](https://t.me/svitsov_site_shot_bot)

## Общее описание
Бот, который присылает скриншот веб - страницы в ответ на присланную боту ссылку.
Тестовое задание для компании True Positive Lab.


## Стэк:

- Python 3.9
- aiogram==3.5.0
- beautifulsoup4==4.12.3
- pillow==10.3.0
- playwright==1.43.0
- Unittest
- Docker
- aiosqlite==0.20.0
- asyncpg==0.29.0

## Запуск проекта в режиме разработки

- Установите и активируйте виртуальное окружение.
- Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
- Создайте файл .env и разместите в нем TOKEN=токен_вашего_бота
- Токен бота вы можете получить https://t.me/BotFather
- Кроме прочего, в случае если вы хотите использовать PostgreSQL, необходимы переменные для работы с этой СУБД.
- После этого вы можете запустить приложение
```
python3 app.py
```

## Запуск проекта с Docker compose
- Перейдите в корневую директорию проекта
- Выполните команду:
```
docker compose up
```
* Важное примечание - должен быть активен docker deamon.


## Важные примечания по проекту (Версия 2)
1) Бот реализован на Python
2) Все настройки бот берет из переменных окружения или .env
файла
3) Бот можно развернуть с помощью Docker образа. Здесь есть важное примечание.*НОВОЕ. Compose up работает хорошо, и все необходимые данные(скриншоты, логи, sqlite бд) сохраняет в том, через папку data. К сожалению не успел настроить PostgreSQL, хоть и принцип его работы очевиден.
Примечание: необходимо было взять готовый образ postgres и добавить в docker-compose:
```
services:
  db:
    image: postgres:13.10
    env_file: .env
    volumes:
      - pg_data:/var/lib/postgresql/data
```
И конечно же указать переменные окружения.
Но к сожалению столкнулся с техническими проблемами на машине, поэтому оставил SQLite.
4) Зависимости бота указаны в requirements.txt
5) Для бота есть инструкция по его развёртыванию в README.md, собственно тут.
6) Бот логгирует свою работу с использованием библиотеки logging. Логи фиксируются как в файл, так и транслируются в терминал. Логи установленны в критеческих точках, и в точках перехода состояния функций/хэндлеров для информативности. *НОВОЕ. Кроме прочего реализовал модели, и теперь все основные логи, связанные с пользователем фиксируются в БД.
7) Перезапуск контейнеров не приводит к потере данных.
8) *НОВОЕ: Процесс получения скриншота более не блокирует поток. Получение WHOIS осталось синхронным, однако его нагрузка в сравнении с получением скриншота ничтожно мала, и практически не влияет на работу бота.
9) *НОВОЕ. У бота появилась возможность выбора языка между Русским и Английским. К сожалению не успел реализовать сохранение состояний в Redis, поэтому на текущий момент выбранный язык устанавливается в переменную.
10) Бот работает и в личных сообщениях и при добавлении в чат. Однако функционал получения скриншота в группе на момент написания этого текста я сформировать не успел. Можно просто задублировать функцию, однако работа в группе более остро требует асинхронного подхода, поэтому поспешный вариант не подходит.
11)  По команде /start бот встречает пользователя сообщением-приветствием,
которое рассказывает о функционале бота.
12) При получении сообщения с ссылкой, бот присылает сообщение заглушку, о том что запрос принят, и запускает процесс получения
скриншота в фоне.
13) Когда скриншот получен, бот редактирует сообщение-заглушку:
  a. Прикрепляет скриншот к сообщению
  b. Заменяет текст сообщения на заголовок сайта, URL и время обработки
  страницы
  c. Добавляет к сообщению кнопку “Подробнее”, которая
  показывает WHOIS сайта, при его наличии.
14) Скриншоты бот так же сохраняет в файловую систему. В имени файла: дата запроса, user_id пользователя, домен из
url запроса.*НОВОЕ. Также реализовано сохранение в БД.
15) У каждого класса и каждой функции есть документ строка. Кроме того в определенных местах скрипта оставлены комментарии для "читабельности" кода.
16) Реализованы Unit тесты для базовых хэндлеров.
17) *НОВОЕ. Запись статистики в БД реализовал через запись логов. Не уверен, что это то, что от меня ждали, однако как мне кажется, с точки зрения аналитики достаточно удобно работать по логам.
18) *НОВОЕ. У проекта 3 ветки помимо основной. first_version - ветка с кодом, отправленным на первое ревью, second_version - ветка с кодом, где реализовано асинхронное получение скриншота, но нет БД. Ветка data_base_version - финальная ветка проекта, она представлена в ветке main.


# Завершение
Это была моя по сути первая работа с ботом, поэтому пришлось учиться на ходу, по документации, видеоурокам и прочему.
В процессе обучения реализовал бота для пиццерии с подключенной PostgreSQL, вот он: 
[![GitHub](https://img.shields.io/badge/GitHub-Kirill--Svitsov-blue)](https://github.com/Kirill-Svitsov/pizzeria_bot)

Конечно, важно отметить, что проект можно улучшить: 
- В первую очередь реализовать ассинхронное получение скриншота, не блокируя поток, что позволит смело добавлять бота в группу.
- Подключить бота к БД и сохранять необходимую информацию, например логи, для последующей аналитики.
- Посмотреть что можно сделать с web драйверами, чтобы "облегчить" образ приложения.
  
Однако на текущий момент я надеюсь, что мой подход к кодированию вам понравился.
