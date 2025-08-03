# 🚀 User Management API

A high-performance, scalable API built with **FastAPI** for managing user data. Features include PostgreSQL for persistence, Redis for caching, rate limiting, and optimized performance for high-load scenarios.

---

## ✨ Features

- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.8+.
- **PostgreSQL**: Robust relational database for persistent user storage.
- **Redis**: In-memory caching to speed up frequent read operations.
- **Rate Limiting**: Protects endpoints using `SlowAPI`.
- **Async Operations**: Non-blocking database queries using `asyncpg`.
- **Gzip Compression**: Reduces response size via FastAPI middleware and Nginx.
- **Fast JSON Serialization**: Uses `orjson` for ultra-fast JSON handling.
- **Load Testing**: Integrated with Locust for performance benchmarking.
- **Dockerized**: Fully containerized for easy setup and deployment.

---

## 🛠️ Setup & Installation

### 1. Install Docker and Docker Compose

Ensure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

### 2. Start PostgreSQL and Redis

```bash
docker-compose up -d   
