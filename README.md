# Название проекта
## 🌐 Обзор
Здесь общее описание проекта

## 📋 Оглавление
- [Функциональность](#-функциональность)
- [Установка и запуск](#️-установка-и-запуск)
- [Стек технологий](#-стек-технологий)
- [Структура проекта](#-структура-проекта)
- [Переменные окружения](#-переменные-окружения)

## 🚀 Функциональность
### 1. Команды бота:  

/start - запуск бота  

### 2. Первая фича:  

**С такими-то опциями**:  
  
Описание
  
**С другими опциями**:  
  
Описание  

### 3. Вторая фича:  
  
Описание  

...  

### 6. Мониторинг и логирование:  

Интеграция с лог-ботом для администрирования ошибок.

## ⚙️ Установка и запуск

1. **Клонирование репозитория**:
   ```bash
   git@github.com:petra-khrushcheva/base_project.git
   cd base_project
   ```

2. **Настройка переменных окружения: создайте файл .env на основе [.env.example](./.env.example) и заполните его необходимыми данными.**

3. **Запуск Docker Compose:**

   ```bash
   docker compose -f docker-compose-dev.yml up
   ```

4. **Запуск бота и сервера: Приложение автоматически запускается при старте Docker Compose.**

5. **Создание аккаунта для доступа к админ-панели:**

   После того, как контейнеры будут запущены, необходимо создать администратора для доступа к админ-панели. Для этого выполните следующие шаги:

   1. Зайдите в контейнер с помощью команды:
      ```bash
      docker exec -it <container_name> sh
      ```
      Пример:
      ```bash
      docker exec -it base_project_backend sh
      ```

   2. Создайте администратора, используя команду:
      ```bash
      python src/manage.py create-admin <admin_name> <admin_password>
      ```
      Пример:
      ```bash
      python src/manage.py create-admin admin password123
      ```
      В результате должно появиться сообщение:
      ```
      New admin created: <admin_name>
      ```
   3. После успешного создания администратора, выйдите из контейнера:
      ```bash
      exit
      ```

   Админка доступна по адресу /admin
   
6. **Создание и применение миграций:**

   Для внесения изменений в структуру базы данных (например, добавление новых колонок, таблиц и т.д.), нужно создать миграцию и применить её. Для этого при запущенных контейнерах выполните следующие шаги:

   1. Зайдите в контейнер с помощью команды:
      ```bash
      docker exec -it <container_name> sh
      ```
      Пример:
      ```bash
      docker exec -it base_project_backend sh
      ```

   2. Создайте миграцию с помощью команды:
      ```bash
      alembic revision --autogenerate -m "<название_миграции>"
      ```
      Пример:
      ```bash
      alembic revision --autogenerate -m "add_some_column_to_some_table"
      ```

   3. Выйдите из контейнера:
      ```bash
      exit
      ```

   4. Перезапустите контейнеры для автоматического применения миграции:
      ```bash
      docker compose -f docker-compose-dev.yml up
      ```


## 🛠 Стек технологий
- **Python**: язык программирования
- **Aiogram**: для создания и управления телеграм-ботом
- **FastAPI**: для управления приложением
- **Aiohttp**: для асинхронных HTTP-запросов
- **PostgreSQL**: реляционная база данных
- **SQLAlchemy**: ORM для взаимодействия с базой данных
- **Redis**: для хранения состояний бота и кэширования данных
- **Alembic**: для управления миграциями базы данных
- **Starlette Admin**: для создания админ-панели
- **Docker**: для контейнеризации
- **S3-совместимое хранилище**: для хранения и получения медиафайлов


## 📁 Структура проекта
```bash
base_project/
├── .github/workflows/             # Конфигурация для CI/CD в GitHub
├── alembic/                       # Файлы миграций
├── src/
│   ├── admin/                     # Настройка админ-панели
│   ├── api/                       # Эндпоинты FastAPI
│   ├── bot/                       # Логика телеграм-бота
│   ├── client/                    # Клиенты для взаимодействия с внешними API и сервисами
│   ├── database/                  # Модели и репозитории базы данных
│   ├── media/                     # Тексты бота
│   ├── scheduled_tasks/           # Периодические задачи
│   ├── services/                  # Бизнес логика 
│   ├── utils/                     # Вспомогательные модули
│   ├── app_manager.py             # Управление жизненным циклом приложения (инициализация, запуск, завершение)
│   ├── config.py                  # Конфигурация приложения
│   ├── main.py                    # Основной файл для запуска приложения
│   ├── manage.py                  # Скрипт для выполнения команд через CLI
│   └── schemas.py                 # Схемы данных
├── .env.example                   # Шаблон файла переменных окружения
├── alembic.ini                    # Конфигурация Alembic для миграций
├── docker-compose-dev.yml         # Docker Compose для разработки
├── docker-compose.yml             # Docker Compose для продакшена
├── Dockerfile                     # Dockerfile для сборки образа
└── requirements.txt               # Список зависимостей проекта
```

## 🔑 Переменные окружения

### PostgreSQL
- `POSTGRES_HOST`: адрес сервера базы данных
- `POSTGRES_PORT`: порт сервера базы данных
- `POSTGRES_DB`: название базы данных
- `POSTGRES_USER`: пользователь базы данных
- `POSTGRES_PASSWORD`: пароль пользователя базы данных

### Redis
- `REDIS_HOST`: адрес сервера Redis
- `REDIS_PORT`: порт сервера Redis
- `REDIS_DB`: номер базы данных Redis (по умолчанию 0)

### Общие настройки
- `API_URL`: адрес внешного API
- `BOT_TOKEN`: токен бота  
- `LOG_BOT_TOKEN`: токен бота для логов  
- `MAINTAINERS_USER_IDS`: список тг-id получателей логов бота

### Безопасность
- `SECRET_KEY`: ключ для шифрования и защиты сессий
- `FORWARDED_ALLOW_IPS`: список IP-адресов, которым разрешено передавать заголовок X-Forwarded-For, используемый для доступа к админке через прокси-сервер

### Настройки S3
- `AWS_ACCESS_KEY_ID`: идентификатор ключа доступа AWS
- `AWS_SECRET_ACCESS_KEY`: секретный ключ доступа AWS
- `S3_BUCKET`: имя S3-бакета
- `S3_ENDPOINT_URL`: URL-адрес API для взаимодействия с S3-совместимым сервисом
- `S3_DOMAIN`: URL-адрес для доступа к объектам

Подробнее — в файле [`.env.example`](./.env.example).