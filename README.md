# Book Management System

A Django-based book management system with PostgreSQL database.

## Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Virtual environment

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create `.env` file with your environment variables (see `.env.example`)

## Running the Application

### Start Database with Docker Compose

```bash
# Start all services
docker compose up -d
```

### Start Django Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run Django development server on port 3000
python manage.py runserver 3000
```

The application will be available at:
- Django API: http://127.0.0.1:3000/
- Adminer (Database Admin): http://localhost:8080/

## Database Migrations

### Create Migrations

```bash
# Create migrations for all apps
python manage.py makemigrations
```

### List Migrations

```bash
# Show all migrations (applied and unapplied)
python manage.py showmigrations
```

### Run Migrations

```bash
# Apply all pending migrations
python manage.py migrate
```

### Revert Migrations

```bash
# Revert to specific migration
python manage.py migrate app_name 0001
```
