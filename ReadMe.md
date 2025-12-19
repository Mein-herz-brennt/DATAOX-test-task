## ⚙️ Налаштування (Environment Variables)

Створіть файл `.env` у кореневій папці проекту:

```env
# Для локального запуску (через PyCharm/Термінал)
DATABASE_URL=postgresql+pg8000://autoria:autoria@localhost:5435/autoria

# Для запуску всередині Docker
DATABASE_URL=postgresql+pg8000://autoria:autoria@db:5432/autoria

# Посилання на головну сторінку 
PAGE_LINK=https://auto.ria.com/uk/car/used/
```
1. Підняття бази даних у Docker
```Bash

docker-compose up -d db
```
2. Запуск міграцій (Alembic)

Створення таблиць у базі даних:
Bash
```
alembic upgrade head
```
Команди Docker Compose

Зібрати та запустити весь проект:
```Bash

docker-compose up --build
```
Повне очищення (видалення контейнерів та дисків з даними):
```Bash

docker-compose down -v
```