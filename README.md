# 🚀 Order Service API

A scalable **FastAPI-based backend** for managing users, orders, and notifications, with support for authentication, pagination, and async database operations.

---

# 🧱 Tech Stack

* ⚡ FastAPI (async web framework)
* 🐘 PostgreSQL
* 🧵 SQLAlchemy (Async ORM)
* 🚀 Uvicorn (ASGI server)
* 🔐 JWT Authentication
* ⚡ Redis (caching / blacklist)
* 🧠 pgvector (for future AI/RAG features)
* 🐇 RabbitMQ (background tasks / messaging)

---

# 📦 Features

## 👤 Users

* Create users
* List users (paginated)

## 📦 Orders

* Create orders
* List orders (paginated)
* Linked to users
* Status tracking:

  * `pending`
  * `completed`
  * `cancelled`

## 🔔 Notifications

* Linked to orders
* Many-to-many with users
* List notifications
* Delete notifications

## 🔐 Authentication

* JWT-based auth
* Access + Refresh tokens
* Logout via token blacklisting (Redis)

---

# 🧩 Data Model Overview

### User

* `id`
* `email`
* `joined_at`
* relationships:

  * orders
  * notifications

### Order

* `id`
* `name`
* `price`
* `status`
* `user_id`
* timestamps

### Notification

* `id`
* `message`
* `order_id`
* many-to-many with users

---

# 🔐 Authentication Flow

1. Login → `/api/v1/auth/token`
2. Receive:

   * `access_token`
   * `refresh_token`
3. Use `Authorization: Bearer <token>`
4. Logout → token added to Redis blacklist

---

# 🌐 API Endpoints

## 🔑 Auth

| Method | Endpoint              | Description  |
| ------ | --------------------- | ------------ |
| POST   | `/api/v1/auth/token`  | Login        |
| GET    | `/api/v1/auth/me`     | Current user |
| GET    | `/api/v1/auth/logout` | Logout       |

---

## 👤 Users

| Method | Endpoint         | Description |
| ------ | ---------------- | ----------- |
| POST   | `/api/v1/users/` | Create user |
| GET    | `/api/v1/users/` | List users  |

---

## 📦 Orders

| Method | Endpoint          | Description  |
| ------ | ----------------- | ------------ |
| POST   | `/api/v1/orders/` | Create order |
| GET    | `/api/v1/orders/` | List orders  |

---

## 🔔 Notifications

| Method | Endpoint                     | Description         |
| ------ | ---------------------------- | ------------------- |
| GET    | `/api/v1/notifications/`     | List notifications  |
| DELETE | `/api/v1/notifications/{id}` | Delete notification |

---

## 🧪 Health

| Method | Endpoint  |
| ------ | --------- |
| GET    | `/health` |
| GET    | `/`       |

---

# 📄 Example Request

## Create Order

```json
POST /api/v1/orders/

{
  "name": "Laptop",
  "price": 1200.50
}
```

---

# ⚙️ Setup & Installation

## 1. Clone repository

```bash
git clone <repo_url>
cd project
```

---

## 2. Install dependencies

```bash
uv sync
uv export --format requirements.txt --no-dev > requirements  # to production
# uv export --format requirements.txt > requirements # to dev
```

---

## 3. Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key
```

---

## 4. Run database migrations

```bash
alembic upgrade head
```

---

## 5. Run the app

```bash
docker compose up --build
```

---

# 🐳 Running with Docker Compose

This project includes a full **containerized environment** with:

* 🚀 FastAPI backend
* 🐘 PostgreSQL
* 🐇 RabbitMQ (message broker)
* ⚡ Redis (cache + blacklist)

---

# ⚙️ Prerequisites

* Docker
* Docker Compose (v2+)

---

# 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=orders_db

# Redis
REDIS_PASSWORD=redispassword
```

---

# 🚀 Build & Run

## 1. Build services

```bash
docker compose build
```

---

## 2. Start all services

```bash
docker compose up
```

Run in background:

```bash
docker compose up -d
```

---

## 3. Stop services

```bash
docker compose down
```

---

# 🌐 Services & Ports

| Service      | URL                        | Description      |
| ------------ | -------------------------- | ---------------- |
| Backend      | http://localhost:8000      | FastAPI app      |
| Swagger Docs | http://localhost:8000/docs | API docs         |
| PostgreSQL   | localhost:5432             | Database         |
| Redis        | localhost:6379             | Cache            |
| RabbitMQ UI  | http://localhost:15672     | Broker dashboard |

---

# 🔐 RabbitMQ Access

* Username: `guest`
* Password: `guest`
* vhost: `my_vhost`

---

# ❤️ Health Checks

* Backend: `/health`
* RabbitMQ: `rabbitmq-diagnostics ping`
* Redis: `redis-cli ping`

---

# 🧪 Verify Everything Is Running

```bash
docker compose ps
```

You should see all services as **healthy**.

---

# 🗄️ Database Setup

If using migrations:

```bash
docker compose exec backend alembic upgrade head
```

---

# 🐚 Access Containers

## Backend shell

```bash
docker compose exec backend bash
```

## PostgreSQL shell

```bash
docker compose exec db psql -U postgres
```

## Redis CLI

```bash
docker compose exec cache_host redis-cli -a $REDIS_PASSWORD
```

---

# 📦 Volumes

| Volume          | Purpose           |
| --------------- | ----------------- |
| `redis_data`    | Redis persistence |
| `rabbitmq_data` | RabbitMQ data     |

> PostgreSQL volume is currently disabled (data will be lost on restart).

---

# ⚠️ Important Notes

### ❗ 1. PostgreSQL persistence disabled

```yaml
# pgdata volume is commented out
```

👉 If you want persistence, enable:

```yaml
volumes:
  - pgdata:/var/lib/postgresql/data
```

---

### ❗ 2. Hot reload enabled

```yaml
volumes:
  - ./:/app
```

👉 Changes in code reflect immediately inside container.

---

### ❗ 3. Service dependencies

* Backend waits for:

  * DB (started)
  * RabbitMQ (healthy)

---

# 🔄 Rebuild After Changes

```bash
docker compose down
docker compose up --build
```

---

# 🧹 Clean Everything

```bash
docker compose down -v
```

👉 Removes:

* containers
* networks
* volumes (⚠️ data loss)

---

# 🚀 Production Tips

* Use `.env.production`
* Enable PostgreSQL volume
* Use proper secrets (not plain `.env`)
* Add reverse proxy (Nginx)

---

# 🧩 Architecture (Docker)

```text
backend (FastAPI)
   ↓
PostgreSQL (db)
Redis (cache)
RabbitMQ (broker)
```

---

# ✅ Summary

With one command:

```bash
docker compose up --build
```

You get a fully working system with:

* API
* DB
* Cache
* Message broker

---

# 🧪 Testing

```bash
pytest
```

---

# 🎯 Future Improvements

* 🧠 AI-powered recommendations (RAG with pgvector)
* 🔄 Background workers (RabbitMQ + Celery)
* 📊 Analytics dashboard
* 📦 Order history personalization
* ⚡ Caching layer optimization

---

# 📚 API Docs

Once running:

* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

---

# 🧠 Architecture

```
FastAPI
   ↓
Service Layer
   ↓
Async SQLAlchemy
   ↓
PostgreSQL + pgvector
   ↓
Redis (cache / blacklist)
   ↓
RabbitMQ (events)
```

---

# ⚠️ Notes

* Uses async everywhere → high performance
* Token blacklist stored in Redis
* Email uniqueness enforced (partial index)
* Pagination supported on all list endpoints

---

# 📄 License

MIT

# Last Word
the project is still in development to integrate AI/ML and create it into a Microservice system.
