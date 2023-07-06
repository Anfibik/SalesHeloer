# Базовый образ
FROM python

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Установка переменных окружения
ENV FLASK_APP=run.py

# Открытие порта
EXPOSE 5000

# Запуск приложения
CMD ["flask", "run", "--host=0.0.0.0"]
