FROM python:3.9-slim

WORKDIR /siteshot_bot

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip3 install -r /siteshot_bot/requirements.txt --no-cache-dir

COPY . .

CMD ["python", "app.py"]