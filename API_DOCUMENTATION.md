# Economic Activities Reporting API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. You need to obtain a token by logging in, then include the token in the Authorization header for all subsequent requests.

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "staff_code": "your_staff_code",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your_refresh_token"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using the Token
Include the access token in the Authorization header:
```bash
-H "Authorization: Bearer your_access_token"
```

---

## Users API

### Get Current User Profile
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer your_access_token"
```

### List All Users (Admin only)
```bash
curl -X GET "http://localhost:8000/api/users/?role=maker&is_active=true" \
  -H "Authorization: Bearer your_access_token"
```

### Get User by ID
```bash
curl -X GET http://localhost:8000/api/users/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Create User (Admin only)
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "staff_code": "EMP001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "role": "maker"
  }'
```

### Update User (Admin only)
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "checker",
    "is_active": true
  }'
```

### Delete User (Admin only)
```bash
curl -X DELETE http://localhost:8000/api/users/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Get User Statistics (Admin only)
```bash
curl -X GET http://localhost:8000/api/users/stats/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Fiscal Years API

### List Fiscal Years
```bash
curl -X GET "http://localhost:8000/api/fiscal-years/?status=approved" \
  -H "Authorization: Bearer your_access_token"
```

### Get Fiscal Year by ID
```bash
curl -X GET http://localhost:8000/api/fiscal-years/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Create Fiscal Year
```bash
curl -X POST http://localhost:8000/api/fiscal-years/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "year": "2081/82"
  }'
```

### Update Fiscal Year
```bash
curl -X PATCH http://localhost:8000/api/fiscal-years/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "year": "2082/83"
  }'
```

### Approve Fiscal Year (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/fiscal-years/1/approve/ \
  -H "Authorization: Bearer your_access_token"
```

### Reject Fiscal Year (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/fiscal-years/1/reject/ \
  -H "Authorization: Bearer your_access_token"
```

### Delete Fiscal Year
```bash
curl -X DELETE http://localhost:8000/api/fiscal-years/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Sectors API

### List Sectors
```bash
curl -X GET "http://localhost:8000/api/sectors/?status=approved" \
  -H "Authorization: Bearer your_access_token"
```

### Get Sector by ID
```bash
curl -X GET http://localhost:8000/api/sectors/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Create Sector
```bash
curl -X POST http://localhost:8000/api/sectors/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Agriculture",
    "description": "Agricultural sector data",
    "has_different_report": false
  }'
```

### Update Sector
```bash
curl -X PATCH http://localhost:8000/api/sectors/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'
```

### Approve Sector (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/sectors/1/approve/ \
  -H "Authorization: Bearer your_access_token"
```

### Reject Sector (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/sectors/1/reject/ \
  -H "Authorization: Bearer your_access_token"
```

### Delete Sector
```bash
curl -X DELETE http://localhost:8000/api/sectors/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Data Categories API

### List Data Categories
```bash
curl -X GET "http://localhost:8000/api/data-categories/?sector=1&status=approved" \
  -H "Authorization: Bearer your_access_token"
```

### Get Data Category by ID
```bash
curl -X GET http://localhost:8000/api/data-categories/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Create Data Category
```bash
curl -X POST http://localhost:8000/api/data-categories/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "sector": 1,
    "name": "Crop Production",
    "parent": null,
    "unit": "MT",
    "is_summable": true
  }'
```

### Create Child Category
```bash
curl -X POST http://localhost:8000/api/data-categories/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "sector": 1,
    "name": "Rice",
    "parent": 1,
    "unit": "MT",
    "is_summable": false
  }'
```

### Get Categories by Sector
```bash
curl -X GET "http://localhost:8000/api/data-categories/by_sector/?sector_id=1" \
  -H "Authorization: Bearer your_access_token"
```

### Approve Category (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/data-categories/1/approve/ \
  -H "Authorization: Bearer your_access_token"
```

### Reject Category (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/data-categories/1/reject/ \
  -H "Authorization: Bearer your_access_token"
```

### Update Data Category
```bash
curl -X PATCH http://localhost:8000/api/data-categories/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "unit": "KG",
    "remarks": "Updated remarks"
  }'
```

### Delete Data Category
```bash
curl -X DELETE http://localhost:8000/api/data-categories/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Places API

### List Places
```bash
curl -X GET "http://localhost:8000/api/places/?state=Bagmati" \
  -H "Authorization: Bearer your_access_token"
```

### Get Place by ID
```bash
curl -X GET http://localhost:8000/api/places/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Create Place
```bash
curl -X POST http://localhost:8000/api/places/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Kathmandu",
    "state": "Bagmati"
  }'
```

### Update Place
```bash
curl -X PATCH http://localhost:8000/api/places/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Kathmandu Valley"
  }'
```

### Delete Place
```bash
curl -X DELETE http://localhost:8000/api/places/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Economic Data Progress API

### List Economic Data Progress
```bash
curl -X GET "http://localhost:8000/api/economic-data-progress/?fiscal_year=1&status=pending" \
  -H "Authorization: Bearer your_access_token"
```

### Get Economic Data Progress by ID
```bash
curl -X GET http://localhost:8000/api/economic-data-progress/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Create Economic Data Progress
```bash
curl -X POST http://localhost:8000/api/economic-data-progress/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "fiscal_year": 1,
    "province": 1,
    "district": 1,
    "municipality": 1,
    "sector": 1,
    "report_type": 1,
    "is_completed": false
  }'
```

### Update Economic Data Progress
```bash
curl -X PATCH http://localhost:8000/api/economic-data-progress/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "is_completed": true
  }'
```

### Approve Progress (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/economic-data-progress/1/approve/ \
  -H "Authorization: Bearer your_access_token"
```

### Reject Progress (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/economic-data-progress/1/reject/ \
  -H "Authorization: Bearer your_access_token"
```

### Mark Progress as Completed
```bash
curl -X POST http://localhost:8000/api/economic-data-progress/1/complete/ \
  -H "Authorization: Bearer your_access_token"
```

### Delete Economic Data Progress
```bash
curl -X DELETE http://localhost:8000/api/economic-data-progress/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Economic Data Entries API

### List Economic Data Entries
```bash
curl -X GET "http://localhost:8000/api/economic-data-entries/?progress=1&status=pending" \
  -H "Authorization: Bearer your_access_token"
```

### Get Economic Data Entry by ID
```bash
curl -X GET http://localhost:8000/api/economic-data-entries/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Create Economic Data Entry
```bash
curl -X POST http://localhost:8000/api/economic-data-entries/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "progress": 1,
    "category": 1,
    "value": 1500.50,
    "capacity": 2000.00
  }'
```

### Update Economic Data Entry
```bash
curl -X PATCH http://localhost:8000/api/economic-data-entries/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "value": 1600.75
  }'
```

### Approve Entry (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/economic-data-entries/1/approve/ \
  -H "Authorization: Bearer your_access_token"
```

### Reject Entry (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/economic-data-entries/1/reject/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "rejected_reason": "Data value is incorrect"
  }'
```

### Delete Economic Data Entry
```bash
curl -X DELETE http://localhost:8000/api/economic-data-entries/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## User Related Offices API

### List User Related Offices
```bash
curl -X GET "http://localhost:8000/api/user-related-offices/?status=approved" \
  -H "Authorization: Bearer your_access_token"
```

### Get User Related Office by ID
```bash
curl -X GET http://localhost:8000/api/user-related-offices/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Create User Related Office
```bash
curl -X POST http://localhost:8000/api/user-related-offices/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "office": "Department of Agriculture"
  }'
```

### Approve Office (Admin/Checker only)
```bash
curl -X POST http://localhost:8000/api/user-related-offices/1/approve/ \
  -H "Authorization: Bearer your_access_token"
```

### Update User Related Office
```bash
curl -X PATCH http://localhost:8000/api/user-related-offices/1/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "office": "Department of Agriculture and Livestock"
  }'
```

### Delete User Related Office
```bash
curl -X DELETE http://localhost:8000/api/user-related-offices/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Report Types API

### List Report Types
```bash
curl -X GET http://localhost:8000/api/report-types/ \
  -H "Authorization: Bearer your_access_token"
```

### Get Report Type by ID
```bash
curl -X GET http://localhost:8000/api/report-types/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Nepali Months API

### List Nepali Months
```bash
curl -X GET "http://localhost:8000/api/nepali-months/?is_first_half=true" \
  -H "Authorization: Bearer your_access_token"
```

### Get Nepali Month by ID
```bash
curl -X GET http://localhost:8000/api/nepali-months/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Address APIs

### List Provinces
```bash
curl -X GET http://localhost:8000/api/provinces/ \
  -H "Authorization: Bearer your_access_token"
```

### Get Province by ID
```bash
curl -X GET http://localhost:8000/api/provinces/1/ \
  -H "Authorization: Bearer your_access_token"
```

### List Districts
```bash
curl -X GET "http://localhost:8000/api/districts/?province=1" \
  -H "Authorization: Bearer your_access_token"
```

### Get District by ID
```bash
curl -X GET http://localhost:8000/api/districts/1/ \
  -H "Authorization: Bearer your_access_token"
```

### List Municipalities
```bash
curl -X GET "http://localhost:8000/api/municipalities/?district=1" \
  -H "Authorization: Bearer your_access_token"
```

### Get Municipality by ID
```bash
curl -X GET http://localhost:8000/api/municipalities/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Notifications API

### List User Notifications
```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Bearer your_access_token"
```

### Get Notification by ID
```bash
curl -X GET http://localhost:8000/api/notifications/1/ \
  -H "Authorization: Bearer your_access_token"
```

### Mark Notification as Read
```bash
curl -X POST http://localhost:8000/api/notifications/1/mark_read/ \
  -H "Authorization: Bearer your_access_token"
```

### Mark All Notifications as Read
```bash
curl -X POST http://localhost:8000/api/notifications/mark_all_read/ \
  -H "Authorization: Bearer your_access_token"
```

### Delete Notification
```bash
curl -X DELETE http://localhost:8000/api/notifications/1/ \
  -H "Authorization: Bearer your_access_token"
```

---

## Dashboard API

### Get Dashboard Data
```bash
curl -X GET http://localhost:8000/api/dashboard/ \
  -H "Authorization: Bearer your_access_token"
```

**Response (Admin):**
```json
{
  "fiscal_years": ["2081/82", "2082/83"],
  "sector_list": ["Agriculture", "Industry"],
  "report_type_list": ["Annual", "First Half"],
  "summary": {
    "total_users": 50,
    "active_sectors": 10,
    "total_entries": 200
  },
  "sector_totals": {
    "Agriculture": 50,
    "Industry": 30
  },
  "system_metrics": {
    "cpu": 45,
    "memory": 60,
    "disk": 30,
    "network": 25
  }
}
```

**Response (Maker):**
```json
{
  "summary": {
    "my_entries": 25,
    "pending": 5,
    "approved": 18,
    "rejected": 2
  }
}
```

**Response (Checker):**
```json
{
  "summary": {
    "pending": 15,
    "reviewed_today": 8,
    "approved": 100,
    "rejected": 5
  }
}
```

---

## Query Parameters

Most list endpoints support the following query parameters:

- **Search**: `?search=keyword` - Search across searchable fields
- **Filtering**: `?field=value` - Filter by specific fields
- **Ordering**: `?ordering=field` or `?ordering=-field` - Order results
- **Pagination**: `?page=1` - Navigate through pages

### Examples:

```bash
# Search users by name
curl -X GET "http://localhost:8000/api/users/?search=john" \
  -H "Authorization: Bearer your_access_token"

# Filter sectors by status and order by name
curl -X GET "http://localhost:8000/api/sectors/?status=approved&ordering=name" \
  -H "Authorization: Bearer your_access_token"

# Get page 2 of results
curl -X GET "http://localhost:8000/api/economic-data-progress/?page=2" \
  -H "Authorization: Bearer your_access_token"
```

---

## Error Responses

The API uses standard HTTP status codes:

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Error Response Format:
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

---

## API Documentation (Swagger)

Interactive API documentation is available at:
```
http://localhost:8000/api/docs/
```

API Schema (JSON) is available at:
```
http://localhost:8000/api/schema/
```

---

## Notes

1. All timestamps are in UTC format
2. All monetary values are stored as Decimal with 2 decimal places
3. Image uploads are supported for sectors (multipart/form-data)
4. Role-based access control:
   - **Admin**: Full access to all endpoints
   - **Checker**: Can approve/reject entries and progress
   - **Maker**: Can create and view their own entries
5. Pagination: Default page size is 20 items per page
6. All endpoints require authentication except login and token refresh


