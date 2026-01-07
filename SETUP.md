# Quick Setup Guide

## Step 1: Environment Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Step 2: Database Setup

1. Create PostgreSQL database:
```bash
createdb economic_activities_api
```

2. Create `.env` file in project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=economic_activities_api
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Step 3: Django Setup

1. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Create superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin user.

## Step 4: Run Server

```bash
python manage.py runserver
```

The API will be available at:
- API Base: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/docs/

## Step 5: Test Authentication

```bash
# Login to get JWT token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "staff_code": "your_staff_code",
    "password": "your_password"
  }'
```

Use the returned `access` token in subsequent requests:
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Next Steps

- See `API_DOCUMENTATION.md` for complete API documentation with all endpoints
- See `README.md` for detailed project information
- Configure your React frontend to use this API


