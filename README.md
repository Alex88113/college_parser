# 🎓 College Parser — Расписание IT-COLLEGE

Асинхронный веб-сервис на FastAPI для получения расписания учебной группы. Интегрируется с внешним API колледжа, кэширует токены в Redis, автоматически обновляет их и отдаёт расписание в удобном HTML-формате.

---

## 🚀 Возможности

- ✅ Авторизация через внешний API колледжа.
- ✅ Автоматическое обновление `access_token` через `refresh_token`.
- ✅ Кэширование токенов и расписания в Redis (с TTL).
- ✅ Отдача расписания на сегодня и завтра в HTML.
- ✅ Reverse-proxy через Nginx.
- ✅ Мониторинг через Prometheus + Grafana.
- ✅ Полная контейнеризация (Docker + Docker Compose).
- ✅ CI/CD через GitHub Actions.
- ✅ Логирование через loguru.

- 🛠️ СТЕК Используемых технологий
text
Python 3.12         — язык разработки
FastAPI             — асинхронный веб-фреймворк
Pydantic            — валидация данных и настройки
httpx               — асинхронный HTTP-клиент
PostgreSQL          — реляционная база данных
asyncpg             — асинхронный драйвер PostgreSQL
Redis               — кэш и хранилище токенов
redis.asyncio       — асинхронный клиент Redis
Docker              — контейнеризация приложения
Docker Compose      — оркестрация сервисов
Nginx               — reverse-proxy
Prometheus          — сбор метрик
Grafana             — визуализация метрик
loguru              — логирование
pytest              — тестирование
respx               — мокирование HTTP-запросов
GitHub Actions      — CI/CD пайплайны

📁 Структура проекта

```text
college_parser/
│
├── 📂 src/college_parser/
│   ├── 🐍 main.py                          # Точка входа FastAPI
│   │
│   ├── 📂 configs/                         # Конфигурации (Pydantic)
│   │   ├── user_config.py                  # Настройки из .env
│   │   ├── redis_config.py                 # Настройки Redis
│   │   └── db_config.py                    # Настройки PostgreSQL
│   │
│   ├── 📂 db/                              # Работа с PostgreSQL
│   │   ├── crud.py                         # CRUD-операции
│   │   └── init_db.py                      # Инициализация БД
│   │
│   ├── 📂 headers/                         # Формирование заголовков
│   │   ├── get_headers.py                  # Заголовки для GET
│   │   └── post_headers.py                 # Заголовки для POST
│   │
│   ├── 📂 models/                          # Pydantic-модели
│   │   ├── post_response.py                # Модель ответа API
│   │   ├── lesson.py                       # Модель занятия
│   │   └── redis_settings_shame.py         # Настройки Redis
│   │
│   ├── 📂 routers/                         # FastAPI-роуты
│   │   ├── today_router.py                 # /schedule/today
│   │   └── tomorrow_router.py              # /schedule/tomorrow
│   │
│   ├── 📂 services/                        # Бизнес-логика
│   │   ├── auth_services.py                # Авторизация, обновление токенов
│   │   ├── redis_service.py                # Работа с Redis
│   │   ├── parser_service.py               # Парсинг расписания
│   │   ├── today_schedule_service.py       # Расписание на сегодня
│   │   ├── tomorrow_schedule_service.py    # Расписание на завтра
│   │   └── get_tokens_service.py           # Получение токенов
│   │
│   └── 📂 utils/                           # Утилиты
│       ├── logger.py                       # Настройка loguru
│       ├── validation_post_response.py     # Валидация POST-ответа
│       └── validation_get_response.py      # Валидация GET-ответа
│
├── 📂 tests/                               # Тесты (pytest + respx)
│
├── 🐳 Dockerfile                           # Сборка образа FastAPI
├── 🐳 docker-compose.yaml                  # Оркестрация сервисов
├── 🐳 infra.yaml                           # Инфраструктура (PostgreSQL, Redis)
├── 🌐 nginx.conf                           # Обратный прокси
├── 📊 prometheus.yml                       # Конфиг мониторинга
├── ⚙️ redis.conf                           # Конфиг Redis
├── 📦 requirements.txt                     # Зависимости
├── 📦 requirements-dev.txt                 # Зависимости для разработки
├── 📦 requirements-testing.txt             # Зависимости для тестов
├── 🚀 run.py                               # Точка входа для запуска
└── 📝 pyproject.toml                       # Метаданные проекта
```
⚙️ Установка и запуск
Требования
Docker и Docker Compose

WSL2 (если Windows)

Python 3.12 (для локальной разработки)

1. Клонировать репозиторий
bash
git clone https://github.com/Alex88113/college_parser.git
cd college_parser
2. Создать .env файл
Скопируй .env.example в .env и заполни своими данными:

bash
cp .env.example .env
Пример .env:

env
# PostgreSQL
PSQL_NAME=postgres
PSQL_PASSWORD=postgres
PSQL_PORT=5432
PSQL_HOST=localhost
COLLEGE_DATABASE=college_parser

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# FastAPI
FASTAPI_PORT=8000
FASTAPI_HOST=0.0.0.0

# Внешнее API колледжа
JOURNAL_NAME=your_login
JOURNAL_PASSWORD=your_password
APP_KEY=your_app_key
AUTH_URL=https://msapi.top-academy.ru/api/v2/auth/login
BASE_URL=https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date
3. Запустить проект
bash
docker compose up -d --build
4. Проверить статус
bash
docker compose ps
Все контейнеры должны быть в статусе Up.

🌐 Эндпоинты
Эндпоинт	Метод	Описание
/	GET	Главная страница
/schedule/today	GET	Расписание на сегодня
/schedule/tomorrow	GET	Расписание на завтра
/docs	GET	Swagger-документация
/metrics	GET	Метрики для Prometheus
Примеры запросов
bash
# Главная страница
curl http://localhost:8000/

# Расписание на сегодня
curl http://localhost:8000/schedule/today

# Расписание на завтра
curl http://localhost:8000/schedule/tomorrow

# Документация (открыть в браузере)
http://localhost:8000/docs
🐳 Docker-инфраструктура
Сервис	Образ	Порт	Назначение
web	Собственный	8000	FastAPI-приложение
nginx	nginx:latest	80	Reverse-proxy
db	postgres:16-alpine	5432	PostgreSQL
redis	redis:alpine	6379	Кэш и токены
prometheus	prom/prometheus	9090	Сбор метрик
grafana	grafana/grafana	3000	Визуализация
Сеть
Все сервисы объединены в сеть app_network (bridge). Контейнеры обращаются друг к другу по именам сервисов.

Volumes
postgres-data — данные PostgreSQL.

redis-data — данные Redis.

grafana_data — дашборды Grafana.

prometheus_data — метрики Prometheus.

📊 Мониторинг
Prometheus: http://localhost:9090

Grafana: http://localhost:3000 (логин/пароль: admin/admin)

Метрики
http_requests_total — количество запросов.

http_request_duration_seconds — время ответа.

process_cpu_seconds_total — нагрузка на процессор.

process_resident_memory_bytes — потребление памяти.

🧪 Тестирование
bash
# Установить зависимости для тестов
pip install -r requirements-testing.txt

# Запустить тесты
pytest

# С покрытием
pytest --cov=src
Структура тестов
text
tests/
├── test_configs/       # Тесты конфигов
├── test_routers/       # Тесты роутов
├── test_services/      # Тесты сервисов
└── mock_test/          # Моки
📝 Логирование
Логи пишутся в src/college_parser/services/logs/. Формат — JSON и текстовый. Используется loguru.

🔧 Устранение неполадок
Проблема	Решение
Порт занят	sudo lsof -i :8000 и убить процесс
Redis не подключается	Проверить REDIS_HOST=redis в .env
Токены не обновляются	docker compose exec redis redis-cli ttl access_token
Nginx отдаёт 502	docker compose logs nginx
Контейнер падает	docker compose logs web --tail 50
📋 Полезные команды
bash
# Логи всех сервисов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f web

# Зайти в контейнер
docker compose exec web sh

# Перезапустить проект
docker compose down && docker compose up -d --build

# Полная очистка (с удалением данных)
docker compose down -v
docker system prune -a -f
🔐 Безопасность
Секреты хранятся в .env (не попадают в Git).

Контейнеры работают от имени непривилегированных пользователей.

Ограничены ресурсы (CPU/RAM) для каждого сервиса.

Redis недоступен извне (только внутри сети).

👨‍💻 Автор
Alex88113

GitHub: @Alex88113

⭐ Если проект был полезен — поставь звезду на GitHub!

