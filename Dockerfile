FROM python:3.9-slim

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir

# Устанавливаем chromium-driver
RUN apt-get update && apt-get install -y chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию и копируем файлы проекта
WORKDIR /siteshot_bot
COPY . .

# Запускаем приложение
CMD ["python", "app.py"]
