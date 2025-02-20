# Messaging Service API

## Stack

- Python 3.12
- Django 5.1.6
- Django REST framework 3.15.2
- PostgreSQL
- Redis
- Celery
- Docker
- Docker Compose

## Запуск проекта

1. Клонировать репозиторий:

```bash
git clone https://github.com/agapoov/messaging_service.git
git clone git@github.com:agapoov/messaging_service.git # Или так
cd messaging_service
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv venv
venv\Scripts\activate
source venv/bin/activate # На Linux/MacOS
```

3. Создать .env файл:

```bash
cp .env.example .env
```

4. Установить зависимости:

```bash
docker-compose up --build
```

5. Создать суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

Сервис будет доступен по адресу: http://localhost:8000

## Примеры запросов

### Создание рассылки

Для создания рассылки необходимо указать хотя бы один параметр фильтрации в поле `filter_params`:
- `tag` - фильтрация по тегу клиента
- `operator_code` - фильтрация по коду оператора

```json
{
   "start_time": "2025-02-20T14:38:27.234Z", // Время начала рассылки UTC
   "end_time": "2025-02-20T15:38:27.234Z", // Время окончания рассылки UTC
   "message_text": "Сообщение", // Текст сообщения
   "filter_params": { // Параметры фильтрации клиентов
   "tag": "example", // Опционально: фильтр по тегу
   "operator_code": "999" // Опционально: фильтр по коду оператора
   }
}
```

### Получение рассылок

```json

```
## API Endpoints

### Аутентификация
- POST `/api/v1/users/register/` - Регистрация пользователя
- POST `/api/token/` - Получение JWT токенов
- POST `/api/token/refresh/` - Обновление токена
- POST `/api/token/verify/` - Проверка токена

### Клиенты
- GET `/api/v1/clients/` - Список клиентов
- POST `/api/v1/clients/` - Создание клиента
- GET `/api/v1/clients/{id}/` - Получение клиента
- PUT `/api/v1/clients/{id}/` - Обновление клиента
- DELETE `/api/v1/clients/{id}/` - Удаление клиента

### Рассылки
- GET `/api/v1/mailing/` - Список рассылок
- POST `/api/v1/mailing/create/` - Создание рассылки
- GET `/api/v1/mailing/{id}/` - Получение рассылки

## Документация API

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Особенности реализации

1. **Валидация номера телефона**
   - Формат: 7XXXXXXXXXX
   - Автоматическое определение кода оператора

2. **Асинхронная обработка**
   - Celery для управления задачами
   - Redis как брокер сообщений

3. **Фильтрация клиентов**
   - По тегу
   - По коду оператора

4. **Время рассылки**
   - Мгновенная отправка если start_time <= now
   - Отложенная отправка через Celery
   - Прекращение отправки после end_time

## Тестирование

Postman коллекция доступна в файле `postman_collection.json`
