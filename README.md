# Deribit Prices (FastAPI + Celery + PostgreSQL)

Сервис для периодического получения **index price** с Deribit и выдачи сохранённых данных через HTTP API.

## Что делает

- Каждую минуту забирает с Deribit **index price** для `btc_usd` и `eth_usd`
- Сохраняет в PostgreSQL:
  - `ticker` (`btc`/`eth`)
  - `price` (число)
  - `ts` (Unix timestamp, seconds)
- Предоставляет внешний API на FastAPI (все методы — **GET**, обязательный query-параметр `ticker`)

## Стек

- **FastAPI** (HTTP API + Swagger)
- **Celery** (периодические задачи)
- **Redis** (broker/backend Celery)
- **PostgreSQL** (хранилище цен)
- **SQLAlchemy** (ORM)
- **aiohttp** (клиент Deribit)

## API

- Swagger UI: `http://localhost:8000/docs`

Эндпоинты (base path: `/api/v1/prices`):
- `GET /all?ticker=btc` — вся история по тикеру
- `GET /last?ticker=btc` — последняя цена
- `GET /by-date?ticker=btc&ts_from=...&ts_to=...` — цены по диапазону timestamp

## Быстрый старт (Docker)

### Требования

- Docker + Docker Compose

### Запуск

Из корня репозитория:

```bash
docker compose up --build
```

Что поднимется:
- `db` (PostgreSQL) — наружу проброшен на `localhost:5433`
- `redis` (Redis) — `localhost:6379`
- `api` (FastAPI) — `localhost:8000`
- `celery_worker` (Celery worker)
- `celery_beat` (Celery beat, расписание раз в минуту)

### Миграции

Миграции применяются автоматически при старте `api`:

- команда в `docker-compose.yaml`: `alembic upgrade head`

Если нужно прогнать вручную внутри контейнера:

```bash
docker compose exec api alembic upgrade head
```

## Запуск без Docker (локально)

### Требования

- Python 3.12
- PostgreSQL
- Redis

### Переменные окружения

Приложение читает переменные из `.env` (файл **игнорируется** git-ом):
```bash
cp .env.example .env
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Миграции

```bash
alembic upgrade head
```

### Запуск API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Запуск Celery

Worker:

```bash
celery -A app.celery_app worker -l info
```

Beat:

```bash
celery -A app.celery_app beat -l info
```

## Тесты (необязательно)

Установить dev-зависимости:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Запуск:

```bash
pytest
```

## Design decisions

### Почему Celery + Redis

- Celery для планирования и исполнения.
- Redis используется как стандартный брокер/результат-бэкенд.

### Почему FastAPI и async-клиент Deribit

- FastAPI даёт быстрое API с автогенерацией OpenAPI/Swagger и хорошей типизацией.
- Клиент Deribit реализован на `aiohttp`, чтобы I/O (HTTP) выполнялся эффективно.

### Почему разные движки БД для API и Celery

- HTTP API использует **асинхронный** драйвер (`asyncpg`) и `AsyncSession`.
- Celery worker по своей природе **синхронный**, поэтому запись в БД из Celery выполнена через **отдельный синхронный SQLAlchemy engine** (через `psycopg2`), а асинхронность остаётся только для HTTP вызовов Deribit.

