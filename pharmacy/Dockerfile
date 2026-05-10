FROM python:3.13-slim 

# PYTHONDONTWRITEBYTECODE=1 не создаёт файлы .pyc 
# PYTHONUNBUFFERED=1 это для вывода логов сразу в консоль без задержки
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# установка зависимостей для postgresql и pillow(media)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# ставим зависимоти для всего приложения
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# копируем весь проект
COPY . /app/