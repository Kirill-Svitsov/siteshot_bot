FROM python:3.9-slim

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir
RUN playwright install
# Устанавливаем chromium-driver
RUN apt-get update && apt-get install -y \
    chromium-driver \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
 && rm -rf /var/lib/apt/lists/*
# RUN apt-get update && apt-get install -y chromium-driver && \
#     rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию и копируем файлы проекта
WORKDIR /siteshot_bot
COPY . .
# docker run --name bot_container --rm -p 8000:8000 -e TOKEN="7165020364:AAE1ARJ5jkM7dueCVKvq9RqkN6BA6vArTmI" siteshot_bot:v2
# Запускаем приложение
CMD ["python", "app.py"]
