FROM python:3.9-slim

WORKDIR /siteshot_bot

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y chromium-driver
# Копируем все остальные файлы проекта в контейнер
COPY . .

# Запускаем приложение
CMD ["python", "app.py"]
