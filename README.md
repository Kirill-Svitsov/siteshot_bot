[![GitHub](https://img.shields.io/badge/GitHub-Kirill--Svitsov-blue)](https://github.com/Kirill-Svitsov)
# Site shot bot 
[![Telegram Badge](https://img.shields.io/badge/-siteshotbot-blue?style=flat&logo=Telegram&logoColor=white)](https://t.me/svitsov_site_shot_bot)

## Общее описание
Тестовое задание для компании True Positive Lab


## Стэк:

- Python 3.9
- aiogram==3.5.0
- beautifulsoup4==4.12.3
- pillow==10.3.0
- selenium==4.19.0
- Unittest
- Docker

## Запуск проекта в режиме разработки

- Установите и активируйте виртуальное окружение.
- Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
- Создайте файл .env и разместите в нем TOKEN=токен_вашего_бота
- Токен бота вы можете получить https://t.me/BotFather
- После этого вы можете запустить приложение
```
python3 app.py
```
## Запуск проекта с помощью Docker image
- Зарегестрируйтесь в Docker и установите десктопное приложение: https://www.docker.com/
- Скачайте Docker браз https://hub.docker.com/repository/docker/svitsov/shot_bot
- С помощью терминала перейдите в директорию, где расположен образ и выполните команду:
```
docker run --name bot_container --rm -p 8000:8000 -e TOKEN="токен_вашего_бота" svitsov/shot_bot:v1
```
Где: 
* --name bot_container - имя будущего контейнера
* --rm - удаление контейнера после завершения его работы
* -p 8000:8000 - соединение портов хоста(вашего пк) и контейнера
* -e TOKEN="токен_вашего_бота"
* svitsov/shot_bot:v1 - имя образа
## Если вы хотите запустить контейнер в режиме сохранения логов/скриншотов
- Создайте docker volume:
```
docker volume create logs_volume
```
- При запуске контейнера вы можете указать Docker volume для монтирования внутрь контейнера в нужную директорию, где будут сохраняться логи. Для этого используйте опцию -v (или --volume) с указанием имени созданного Docker volume и пути в контейнере, куда он должен быть смонтирован
```
docker run --name bot_container --rm -p 8000:8000 -v logs_volume:/logs -e TOKEN="токен_вашего_бота" svitsov/shot_bot:v1
```

## Важные примечания по проекту
1) Бот реализован на Python
2) Все настройки бот берет из переменных окружения или .env
файла
3) Бот можно развернуть с помощью Docker образа. Здесь есть важное примечание. Образ получился достаточно большим, в связи с использованием библиотеки selenium, которая в свою очередь использует web драйверы для получения скриншота. Была идея разделить свой проект, а web драйверы взять из образа selenium/standalone-chrome, однако в итоге получилось бы тоже самое, с отдельными плюсами и минусами.
4) Зависимости бота указаны в requirements.txt
5) Для бота есть инструкция по его развёртыванию в README.md, собственно тут.
6) Бот логгирует свою работу с использованием библиотеки logging. Логи фиксируются как в файл, так и транслируются в терминал. Логи установленны в критеческих точках, и в точках перехода состояния функций/хэндлеров для информативности.
7) Перезапуск контейнеров не приводит к потере данных в случае использования docker volume. Выше в примере показано, как сохранить логи.
8) К сожалению процесс получения скриншота блокирует поток, так как библиотека selenium синхронная.
9) Бот работает и в личных сообщениях и при добавлении в чат. Однако функционал получения скриншота в группе на момент написания этого текста я сформировать не успел. Можно просто задублировать функцию, однако работа в группе более остро требует асинхронного подхода, поэтому поспешный вариант не подходит.
10)  По команде /start бот встречает пользователя сообщением-приветствием,
которое рассказывает о функционале бота.
11) При получении сообщения с ссылкой, бот присылает сообщение заглушку, о том что запрос принят, и запускает процесс получения
скриншота в фоне.
12) Когда скриншот получен, бот редактирует сообщение-заглушку:
  a. Прикрепляет скриншот к сообщению
  b. Заменяет текст сообщения на заголовок сайта, URL и время обработки
  страницы
  c. Добавляет к сообщению кнопку “Подробнее”, которая
  показывает WHOIS сайта, при его наличии.
13) Скриншоты бот так же сохраняет в файловую систему. В имени файла: дата запроса, user_id пользователя, домен из
url запроса.
14) У каждого класса и каждой функции есть документ строка. Кроме того в определенных местах скрипта оставлены комментарии для "читабельности" кода.
15) Реализованы Unit тесты для базовых хэндлеров.


# Завершение
Это была моя по сути первая работа с ботом, поэтому пришлось учиться на ходу, по документации, видеоурокам и прочему.
В процессе обучения реализовал бота для пиццерии с подключенной PostgreSQL, вот он: 
[![GitHub](https://img.shields.io/badge/GitHub-Kirill--Svitsov-blue)](https://github.com/Kirill-Svitsov/pizzeria_bot)

Конечно, важно отметить, что проект можно улучшить: 
- В первую очередь реализовать ассинхронное получение скриншота, не блокируя поток, что позволит смело добавлять бота в группу.
- Подключить бота к БД и сохранять необходимую информацию, например логи, для последующей аналитики.
- Посмотреть что можно сделать с web драйверами, чтобы "облегчить" образ приложения.
  
Однако на текущий момент я надеюсь, что мой подход к кодированию вам понравился.
