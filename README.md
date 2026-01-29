# DigitalCore Backend

Production-ready Django backend for the DigitalCore Solutions frontend.

## Tech Stack
-   **Language**: Python 3.12+
-   **Framework**: Django 5.0+, Django REST Framework
-   **Database**: SQLite (default) / PostgreSQL (production ready)
-   **Auth**: JWT (SimpleJWT)

## Setup Instructions

1.  **Create Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Create Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run Server**:
    ```bash
    python manage.py runserver
    ```

## API Documentation

The API is versioned at `/api/v1/`.

### Authentication
-   `POST /api/v1/auth/login/` - Get JWT Token given `{email, password}`
-   `POST /api/v1/auth/logout/` - Logout (Blacklist token)
-   `GET /api/v1/auth/me/` - Get current user details

### Projects (`/api/v1/projects/`)
-   `GET /` - List all projects
-   `POST /` - Create project (Admin)
-   `GET /{id}/` - Get project details
-   `PUT /{id}/` - Update project (Admin)
-   `DELETE /{id}/` - Delete project (Admin)

### Services (`/api/v1/services/`)
-   `GET /` - List all services
-   `POST /` - Create service (Admin)
-   `PUT /{id}/` - Update service (Admin)

### Blogs (`/api/v1/blogs/`)
-   `GET /` - List all blogs
-   `GET /slug/{slug}/` - Get blog by slug
-   `POST /` - Create blog (Admin)

### Messages (`/api/v1/messages/`)
-   `POST /` - Send new message (Public)
-   `GET /` - List messages (Admin)
-   `PUT /{id}/read/` - Mark as read (Admin)

### Settings (`/api/v1/settings/`)
-   `GET /` - Get site settings
-   `PUT /` - Update site settings (Admin)

## Frontend Integration
To connect the existing frontend, update `frontend/src/services/api.js` to replace the `mockDelay` and `localStorage` logic with actual Axios calls to these endpoints.

## Environment Variables
Create a `.env` file in `backend/`:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```
