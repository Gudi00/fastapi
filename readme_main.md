# FastAPI Social Media Backend

> Полноценный REST API для социальной сети: посты, пользователи, лайки — собранный на FastAPI с нуля.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/Gudi00/fastapi)
![Stars](https://img.shields.io/github/stars/Gudi00/fastapi?style=social)

---

## 📖 Описание

Это backend-приложение на FastAPI, реализующее базовую функциональность социальной сети: регистрация и аутентификация пользователей, создание постов, система голосований (лайков). Проект построен на PostgreSQL с ORM SQLAlchemy, управлением миграциями через Alembic и JWT-аутентификацией. Код покрыт тестами с помощью pytest и поддерживает развёртывание через Docker.

## 💡 Как появилась идея

> 📝 TODO: опиши своими словами, почему ты выбрал именно этот проект для изучения FastAPI — что тебя привлекло, какую задачу ты хотел решить или какой навык освоить.

Проект построен по материалам YouTube-курса Sanjeev Thiyagarajan по FastAPI. Идея — собрать реалистичный API с нуля, охватив все ключевые концепции: маршрутизацию, схемы данных, работу с базой данных, аутентификацию и тестирование.

---

## 🛠 Технологический стек

| Технология | Версия | Для чего используется |
|---|---|---|
| **FastAPI** | 0.115.12 | Основной веб-фреймворк для построения REST API |
| **Uvicorn** | 0.34.2 | ASGI-сервер для запуска приложения |
| **SQLAlchemy** | 2.0.40 | ORM и SQL-toolkit для работы с БД |
| **PostgreSQL** | 12+ | Реляционная база данных |
| **psycopg2** | 2.9.10 | Адаптер PostgreSQL для Python |
| **Alembic** | 1.15.2 | Управление миграциями схемы БД |
| **Pydantic** | 2.11.3 | Валидация данных и схемы запросов/ответов |
| **passlib + bcrypt** | 1.7.4 / 4.3.0 | Хэширование паролей |
| **python-jose / PyJWT** | — / 2.10.1 | JWT-токены для аутентификации |
| **python-dotenv** | 1.1.0 | Управление переменными окружения |
| **pytest + httpx** | — / 0.28.1 | Тестирование API |
| **Docker + Compose** | — | Контейнеризация и развёртывание |

### Интересные библиотеки

- **Pydantic v2** — новая версия с полностью переписанным ядром (`pydantic-core` на Rust), даёт значительный прирост производительности валидации по сравнению с v1.
- **Alembic** — позволяет версионировать схему базы данных и откатываться к любой миграции, как git для БД.
- **passlib** — абстракция над алгоритмами хэширования, позволяет безболезненно менять алгоритм в будущем без переписывания кода.

---

## ✨ Возможности

- **Регистрация пользователей** — создание аккаунта с email и паролем (bcrypt-хэширование)
- **JWT-аутентификация** — вход через `/login`, получение Bearer-токена, автоматическое истечение
- **CRUD постов** — создание, чтение, обновление, удаление; только владелец может изменять свой пост
- **Поиск и пагинация** — фильтрация постов по заголовку, параметры `limit` и `skip`
- **Система голосований** — лайк/дизлайк поста, один голос на пользователя (составной ключ на уровне БД)
- **Агрегация голосов** — количество лайков возвращается вместе с каждым постом
- **Автоматические миграции** — 8 версий Alembic от начальной схемы до финальной
- **Docker-развёртывание** — отдельные конфигурации для dev и prod окружений
- **Полноценные тесты** — pytest-сьют с изолированной тестовой БД, fixtures, проверкой авторизации
- **CORS** — настроен для приёма запросов с любого источника (подходит для разработки)
- **Интерактивная документация** — Swagger UI и ReDoc из коробки

---

## 🚀 Установка и запуск

### Вариант 1: Локальный запуск

**Требования:** Python 3.9+, PostgreSQL 12+

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Gudi00/fastapi.git
cd fastapi/fastapi-course

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Создать базу данных PostgreSQL
psql -U postgres -c "CREATE DATABASE fastapi;"

# 4. Создать файл .env в папке app/
cat > app/.env << 'EOF'
SQLALCHEMY_DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=300
EOF

# 5. Применить миграции
alembic upgrade head

# 6. Запустить сервер
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000`

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

### Вариант 2: Docker (dev)

```bash
cd fastapi/fastapi-course

# Запустить с PostgreSQL в одном compose
docker-compose -f docker-compose-dev.yml up --build
```

### Вариант 3: Docker (prod)

```bash
# Создать .env с переменными окружения, затем:
docker-compose -f docker-compose-prod.yml up -d
```

---

### Запуск тестов

```bash
cd fastapi/fastapi-course

# Создать тестовую БД
psql -U postgres -c "CREATE DATABASE fastapi_test;"

# Запустить тесты
pytest tests/ -v
```

---

## 📸 Скриншоты и демо

<!-- SCREENSHOT: Swagger UI — главная страница с полным списком эндпоинтов: /posts, /users, /login, /vote -->
![Swagger UI](screenshots/screenshot_1.png)

<!-- SCREENSHOT: Запрос POST /login — форма ввода email и пароля, ответ с JWT access_token -->
![Авторизация](screenshots/screenshot_2.png)

<!-- SCREENSHOT: Запрос GET /posts/ — список постов с количеством лайков (поле votes), параметры limit/skip/search -->
![Список постов](screenshots/screenshot_3.png)

<!-- SCREENSHOT: Запрос POST /posts/ — создание нового поста (требует Bearer-токен в заголовке) -->
![Создание поста](screenshots/screenshot_4.png)

<!-- SCREENSHOT: Запрос POST /vote/ — тело запроса {"post_id": 1, "dir": 1}, ответ об успешном голосовании -->
![Голосование](screenshots/screenshot_5.png)

<!-- SCREENSHOT: Вывод pytest — результаты прохождения всех тестов (test_posts, test_users, test_votes, test_calculations) -->
![Тесты](screenshots/screenshot_6.png)

<!-- SCREENSHOT: Docker Desktop или docker ps — запущенные контейнеры fastapi-app и postgres -->
![Docker](screenshots/screenshot_7.png)

---

## 💼 Как я использую этот проект

> 📝 TODO: опиши конкретные сценарии — используешь ли этот проект как шаблон для других API, как учебный пример, или как основу для чего-то большего?

---

## 👥 Аудитория и пользователи

Проект ориентирован на разработчиков, изучающих FastAPI, Python backend и REST API. Подойдёт как:

- **Стартовая точка** для создания собственного backend-приложения
- **Учебный пример** всех ключевых концепций FastAPI в одном проекте
- **Референс** для паттернов: JWT-аутентификация, PostgreSQL + SQLAlchemy, Alembic-миграции, Docker-деплой

> 📝 TODO: укажи реальное количество пользователей/загрузок, звёзд на GitHub, если проект публичный.

---

## ⚙️ Как реализован проект

### Архитектура

Приложение построено по принципу разделения ответственности:

```
app/
├── main.py       # Инициализация FastAPI, подключение роутеров, CORS
├── models.py     # SQLAlchemy-модели (таблицы users, posts, votes)
├── schemas.py    # Pydantic-схемы для валидации запросов и ответов
├── database.py   # Подключение к PostgreSQL, engine, SessionLocal
├── oauth2.py     # JWT: создание и верификация токенов
├── config.py     # Pydantic Settings — переменные окружения из .env
├── utils.py      # Хэширование и верификация паролей
└── routers/      # Роутеры по доменам (post, user, auth, vote)
```

### Ключевые технические решения

**База данных**

Три таблицы с правильными внешними ключами и `ON DELETE CASCADE`:

```sql
-- Пользователи
users (id, email UNIQUE, password, created_at)

-- Посты с привязкой к владельцу
posts (id, title, content, published, created_at, owner_id → users.id)

-- Голоса: составной первичный ключ гарантирует один голос на пользователя
votes (user_id → users.id, post_id → posts.id, PRIMARY KEY (user_id, post_id))
```

**JWT-аутентификация**

```python
# oauth2.py — создание токена
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_jwt = jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Зависимость FastAPI — автоматически проверяет токен в каждом защищённом роуте
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    ...
```

**Агрегация голосов**

Количество лайков считается через SQL `JOIN` + `func.count()` прямо в запросе:

```python
# routers/post.py
posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
    .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
    .group_by(models.Post.id)\
    .all()
```

**Миграции Alembic**

8 версий миграций отслеживают эволюцию схемы — от начальной таблицы posts до финальной схемы с users, votes и внешними ключами. Это позволяет воспроизвести любое состояние базы данных.

**Тестирование**

Тесты используют отдельную тестовую БД с полным сбросом между тестами через `conftest.py`:

```python
# conftest.py — изоляция тестов
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 🧗 Трудности при разработке

> 📝 TODO: опиши 2-3 сложности, с которыми ты столкнулся при разработке этого проекта. Например: настройка Alembic с переменными окружения, изоляция тестовой базы данных, корректная обработка JWT-ошибок, конфигурация Docker Compose для dev/prod окружений.

---

## 🔮 Планы развития

> 📝 TODO: опиши как планируешь развивать проект. Например: добавить комментарии к постам, систему подписок на пользователей, загрузку изображений, кэширование через Redis, rate limiting, CI/CD pipeline.

---

## 📄 Лицензия

Распространяется под лицензией MIT. Подробнее см. файл [LICENSE](LICENSE).
