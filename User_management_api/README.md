User Management API
A performant FastAPI-based API for managing users, with PostgreSQL, Redis caching, and rate limiting.
Setup

Install Docker and Docker Compose:

Follow instructions at Docker.


Start PostgreSQL and Redis:
docker-compose up -d


Create Database Table:
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);


Install Python Dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


Run the Application:
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app


Test with Locust:
locust -f locustfile.py --host=http://localhost:8000

Open http://localhost:8089 to run load tests.

Access API:

Swagger UI: http://localhost:8000/docs
Example endpoints:
POST /users/: Create a user
GET /users/{id}: Get a user
GET /users/?page=1&page_size=10: List users





Optimizations

Async database queries with asyncpg.
Redis caching for user data.
Rate limiting with slowapi.
Gzip compression in FastAPI and Nginx.
Fast JSON serialization with orjson.
