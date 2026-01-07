# Economic Activities Reporting API

A Django REST Framework API for the Economic Activities Reporting System. This API provides endpoints for managing economic data, users, sectors, fiscal years, and more.

## Features

- JWT Authentication
- Role-based access control (Admin, Maker, Checker)
- RESTful API endpoints
- Comprehensive filtering, searching, and pagination
- Interactive API documentation (Swagger)
- CORS support for React frontend

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## Installation

1. Clone or navigate to the project directory:
```bash
cd Economic-Activities-API
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the project root (see `.env.example`):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=economic_activities_api
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

6. Create the database:
```bash
# Create PostgreSQL database
createdb economic_activities_api
```

7. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

8. Create a superuser:
```bash
python manage.py createsuperuser
```

9. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Documentation

- **Interactive Documentation (Swagger)**: http://localhost:8000/api/docs/
- **API Schema (JSON)**: http://localhost:8000/api/schema/
- **Full API Documentation with cURL examples**: See `API_DOCUMENTATION.md`

## Project Structure

```
Economic-Activities-API/
├── api/                    # Main API application
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views and viewsets
│   ├── urls.py            # URL routing
│   └── admin.py           # Django admin configuration
├── api_project/           # Django project settings
│   ├── settings.py        # Project settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── API_DOCUMENTATION.md   # Complete API documentation
└── README.md             # This file
```

## API Endpoints Overview

### Authentication
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/refresh/` - Refresh access token

### Users
- `GET /api/users/` - List users
- `GET /api/users/me/` - Get current user profile
- `GET /api/users/{id}/` - Get user by ID
- `POST /api/users/` - Create user (Admin only)
- `PATCH /api/users/{id}/` - Update user (Admin only)
- `DELETE /api/users/{id}/` - Delete user (Admin only)
- `GET /api/users/stats/` - Get user statistics (Admin only)

### Fiscal Years
- `GET /api/fiscal-years/` - List fiscal years
- `POST /api/fiscal-years/` - Create fiscal year
- `POST /api/fiscal-years/{id}/approve/` - Approve fiscal year
- `POST /api/fiscal-years/{id}/reject/` - Reject fiscal year

### Sectors
- `GET /api/sectors/` - List sectors
- `POST /api/sectors/` - Create sector
- `POST /api/sectors/{id}/approve/` - Approve sector
- `POST /api/sectors/{id}/reject/` - Reject sector

### Data Categories
- `GET /api/data-categories/` - List categories
- `POST /api/data-categories/` - Create category
- `GET /api/data-categories/by_sector/` - Get categories by sector
- `POST /api/data-categories/{id}/approve/` - Approve category
- `POST /api/data-categories/{id}/reject/` - Reject category

### Economic Data Progress
- `GET /api/economic-data-progress/` - List progress entries
- `POST /api/economic-data-progress/` - Create progress entry
- `POST /api/economic-data-progress/{id}/approve/` - Approve progress
- `POST /api/economic-data-progress/{id}/reject/` - Reject progress
- `POST /api/economic-data-progress/{id}/complete/` - Mark as completed

### Economic Data Entries
- `GET /api/economic-data-entries/` - List entries
- `POST /api/economic-data-entries/` - Create entry
- `POST /api/economic-data-entries/{id}/approve/` - Approve entry
- `POST /api/economic-data-entries/{id}/reject/` - Reject entry

### Address APIs
- `GET /api/provinces/` - List provinces
- `GET /api/districts/` - List districts
- `GET /api/municipalities/` - List municipalities

### Dashboard
- `GET /api/dashboard/` - Get dashboard data (role-based)

### Notifications
- `GET /api/notifications/` - List user notifications
- `POST /api/notifications/{id}/mark_read/` - Mark notification as read
- `POST /api/notifications/mark_all_read/` - Mark all as read

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer your_access_token_here
```

## Role-Based Access Control

- **Admin**: Full access to all endpoints
- **Checker**: Can approve/reject entries and progress, view all data
- **Maker**: Can create and view their own entries only

## Filtering, Searching, and Pagination

Most list endpoints support:
- **Search**: `?search=keyword`
- **Filtering**: `?field=value`
- **Ordering**: `?ordering=field` or `?ordering=-field`
- **Pagination**: `?page=1`

## Testing the API

You can test the API using:
1. **cURL**: See `API_DOCUMENTATION.md` for examples
2. **Swagger UI**: http://localhost:8000/api/docs/
3. **Postman**: Import the API schema from http://localhost:8000/api/schema/
4. **React Frontend**: Configure your React app to use this API

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Set a strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Set up a production database
5. Configure static files serving
6. Set up SSL/HTTPS
7. Configure CORS for your frontend domain

## Support

For detailed API documentation with cURL examples, see `API_DOCUMENTATION.md`.

## License

[Your License Here]


