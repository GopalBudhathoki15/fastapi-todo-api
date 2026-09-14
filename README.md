# FastAPI Todo API

A RESTful Todo API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. The project includes user authentication, JWT-based authorization, per-user task ownership, database migrations, automated tests, and production deployment.

## Features

- User registration
- Secure password hashing
- User login with JWT authentication
- Protected API endpoints
- Create, read, update, and delete tasks
- Per-user task ownership
- Users cannot access, update, or delete another user's tasks
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- Automated API tests with pytest
- Production deployment on Render

## Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **PyJWT**
- **pwdlib / Argon2**
- **pytest**
- **Uvicorn**

## Project Structure

```text id="ng8x9k"
todo_fastapi/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── routers/
│   ├── tests/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
├── .gitignore
├── alembic.ini
└── requirements.txt
```

## Authentication

The API uses JWT bearer authentication.

After successfully logging in, the API returns an access token:

```json id="p4vgw3"
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

Protected endpoints require the token in the `Authorization` header:

```text id="7a8glo"
Authorization: Bearer <access_token>
```

## Task Authorization

Tasks belong to individual users.

A user can only:

- View their own tasks
- Create tasks for themselves
- Update their own tasks
- Delete their own tasks

Task queries are scoped using the authenticated user's ID, preventing users from accessing tasks belonging to other accounts.

## Local Setup

Clone the repository:

```bash id="pxh3lb"
git clone <repository-url>
cd todo_fastapi
```

Create and activate a virtual environment:

```bash id="9y9jma"
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash id="eim26s"
pip install -r requirements.txt
```

Create a `.env` file:

```env id="xwejtu"
DATABASE_URL=postgresql+psycopg://username@localhost:5432/todo_fastapi
TEST_DATABASE_URL=postgresql+psycopg://username@localhost:5432/todo_fastapi_test
SECRET_KEY=your-secret-key
```

Replace these values with your own PostgreSQL credentials and secret key.

## Database Migrations

Apply all Alembic migrations:

```bash id="1safp4"
alembic upgrade head
```

## Running the Application

Start the development server:

```bash id="h1n6bo"
uvicorn app.main:app --reload
```

The API will be available at:

```text id="hm8d7s"
http://localhost:8000
```

Interactive Swagger documentation:

```text id="zck5ij"
http://localhost:8000/docs
```

## Running Tests

Make sure your test PostgreSQL database exists and `TEST_DATABASE_URL` is configured.

Run:

```bash id="mz1pge"
pytest -v
```

The test suite covers authentication, task CRUD operations, and task ownership/authorization.

## Deployment

The application is deployed on **Render** using a managed PostgreSQL database.

The production startup command applies database migrations before starting the API:

```bash id="o90uw5"
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Production values such as `DATABASE_URL` and `SECRET_KEY` are configured as environment variables and are not committed to the repository.

## Project Status

**Completed — v1.0**

The intended scope of this project is complete. It was built as a practical backend project to learn and apply FastAPI, relational databases, authentication, authorization, database migrations, automated testing, Git/GitHub, and production deployment.
