# DigitalCore Backend - Version 1.0 Implementation Plan

**Project:** DigitalCore Solutions Backend API  
**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** January 29, 2026

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Implemented Features](#implemented-features)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Authentication & Authorization](#authentication--authorization)
8. [Deployment Configuration](#deployment-configuration)
9. [Development Setup](#development-setup)

---

## Project Overview

DigitalCore Backend is a **production-ready Django REST API** serving as the backend for DigitalCore Solutions - a digital agency portfolio and business management system. The platform enables management of projects, services, blogs, client messages, and site-wide configuration through a RESTful API with JWT authentication.

### Purpose
- Portfolio showcase management
- Service offerings catalog
- Blog/content publishing system
- Client inquiry handling
- Site-wide settings configuration
- Admin dashboard support

---

## Tech Stack

### Core Framework
- **Python:** 3.12+
- **Django:** 5.0+
- **Django REST Framework (DRF):** 3.14.0+
- **Database:** SQLite (development) / PostgreSQL (production-ready)

### Authentication
- **JWT:** djangorestframework-simplejwt 5.3.1+
- **Token-based authentication** with refresh capabilities

### Key Dependencies
```
Django>=5.0
djangorestframework>=3.14.0
djangorestframework-simplejwt>=5.3.1
django-cors-headers>=4.3.1
Pillow>=10.2.0
python-dotenv>=1.0.1
psycopg2-binary>=2.9.9
gunicorn>=21.2.0
whitenoise>=6.6.0
dj-database-url
```

### Production Features
- **Gunicorn:** WSGI HTTP Server
- **WhiteNoise:** Static file serving with compression
- **CORS:** Enabled for frontend integration
- **Environment-based configuration:** Using python-dotenv

---

## Architecture

### Layer Structure

The project follows Django's **modular app architecture** with a **3-layer pattern**:

```
┌─────────────────────────────────────┐
│         API Layer (Views)           │
│  - HTTP Request/Response Handling   │
│  - Permission Checks                │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    Business Logic (Services)        │
│  - Data Processing                  │
│  - Business Rules                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      Data Layer (Models)            │
│  - Database Schema                  │
│  - Data Validation                  │
└─────────────────────────────────────┘
```

### Project Structure

```
WeboraBackend/
├── config/                    # Main Django configuration
│   ├── settings.py           # App settings, database, middleware
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI application
│
├── apps/                      # Django apps (modular features)
│   ├── accounts/             # User authentication & management
│   │   ├── models.py         # Custom User model
│   │   ├── views.py          # Auth endpoints
│   │   ├── serializers.py    # Data serialization
│   │   ├── services.py       # User business logic
│   │   └── urls.py           # Auth routes
│   │
│   ├── projects/             # Portfolio projects
│   │   ├── models.py         # Project model
│   │   ├── views.py          # CRUD operations
│   │   ├── serializers.py
│   │   ├── services.py
│   │   └── urls.py
│   │
│   ├── services/             # Service offerings
│   ├── blogs/                # Blog/content system
│   ├── contacts/             # Contact messages
│   └── site_settings/        # Global site config
│
├── media/                     # User-uploaded files
├── staticfiles/              # Collected static files
├── db.sqlite3                # SQLite database (development)
├── manage.py                 # Django management script
├── seed_data.py              # Database seeding script
├── build.sh                  # Production build script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── README.md                 # Project documentation
└── DATABASE_SWITCHING_GUIDE.md  # DB migration guide
```

---

## Implemented Features

### ✅ 1. User Authentication & Authorization (`apps.accounts`)

**Custom User Model:**
- Email-based authentication (email as username)
- Role-based access control (admin/user)
- Extends Django's AbstractUser

**Features:**
- JWT token authentication (access + refresh tokens)
- Secure login/logout
- User profile retrieval
- Two-step admin creation with OTP simulation
- Token blacklisting on logout

**Capabilities:**
- 1-day access token lifetime
- 7-day refresh token lifetime
- Custom JWT claims with user data

---

### ✅ 2. Projects Management (`apps.projects`)

**Purpose:** Manage portfolio projects and case studies

**Model Fields:**
- Title, category, description
- Challenge/problem statement
- Image upload support
- Tech stack (JSON array)
- Live link URL
- Featured flag

**Features:**
- Full CRUD operations
- Public read access
- Admin-only create/update/delete
- Image uploads to `media/projects/`
- Featured projects filtering

---

### ✅ 3. Services Catalog (`apps.services`)

**Purpose:** Manage service offerings

**Model Fields:**
- Title, icon (string identifier)
- Short description (preview)
- Full description
- Benefits list (JSON array)
- Process steps (JSON array)
- Active/inactive toggle

**Features:**
- CRUD operations
- Active/inactive filtering
- Structured data for benefits and processes

---

### ✅ 4. Blog System (`apps.blogs`)

**Purpose:** Content publishing and blog management

**Model Fields:**
- Title, unique slug
- Excerpt, full content
- Author, category
- Tags (JSON array)
- Featured image upload
- Auto-generated published date
- Read time estimation

**Features:**
- Slug-based routing (`/blogs/slug/{slug}/`)
- Featured image uploads
- Tag-based organization
- Auto-timestamping
- Full CRUD operations

---

### ✅ 5. Contact Messages (`apps.contacts`)

**Purpose:** Handle client inquiries

**Model Fields:**
- Name, email, subject
- Message content
- Created timestamp
- Read/unread status

**Features:**
- Public message submission
- Admin-only message listing
- Mark messages as read
- Timestamp tracking

---

### ✅ 6. Site Settings (`apps.site_settings`)

**Purpose:** Global site configuration (singleton pattern)

**Model Fields:**
- Company name, tagline
- Contact email, phone, address
- Social media links (JSON)
- Hero section data (JSON)
- About section (JSON)

**Features:**
- Single instance enforcement
- JSON-based flexible configuration
- Site-wide branding control
- Social media integration

**Current Default Values:**
- Company: DigitalCore Solutions
- Email: info@digitalcoresolutions.com
- Tagline: "Building Your Digital Presence"

---

## Database Schema

### User Model
```python
User (Custom AbstractUser)
├── email (EmailField, unique) ← USERNAME_FIELD
├── username (CharField)
├── name (CharField)
├── role (CharField: admin/user)
└── password (hashed)
```

### Project Model
```python
Project
├── title (CharField)
├── category (CharField)
├── description (TextField)
├── challenge (TextField)
├── image (ImageField: media/projects/)
├── techStack (JSONField: array)
├── liveLink (URLField)
└── featured (BooleanField)
```

### Service Model
```python
Service
├── title (CharField)
├── icon (CharField)
├── shortDescription (TextField)
├── description (TextField)
├── benefits (JSONField: array)
├── process (JSONField: array)
└── active (BooleanField)
```

### Blog Model
```python
Blog
├── title (CharField)
├── slug (SlugField, unique)
├── excerpt (TextField)
├── content (TextField)
├── author (CharField)
├── category (CharField)
├── tags (JSONField: array)
├── featuredImage (ImageField: media/blogs/)
├── publishedDate (DateField, auto)
└── readTime (CharField)
```

### Message Model
```python
Message
├── name (CharField)
├── email (EmailField)
├── subject (CharField)
├── message (TextField)
├── createdAt (DateTimeField, auto)
└── read (BooleanField)
```

### SiteSetting Model (Singleton)
```python
SiteSetting
├── companyName (CharField)
├── tagline (CharField)
├── email (EmailField)
├── phone (CharField)
├── address (TextField)
├── social (JSONField: dict)
├── hero (JSONField: dict)
└── about (JSONField: dict)
```

---

## API Endpoints

All endpoints are versioned under `/api/v1/`

### Authentication (`/api/v1/auth/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/login/` | Obtain JWT token + user data | Public |
| GET | `/me/` | Get current user profile | Authenticated |
| POST | `/logout/` | Blacklist token | Authenticated |
| POST | `/create-admin-step1/` | Admin registration (OTP request) | Public |
| POST | `/create-admin-step2/` | Admin registration (OTP verification) | Public |

**Login Request:**
```json
{
  "email": "admin@digitalcore.com",
  "password": "admin123"
}
```

**Login Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "admin@digitalcore.com",
    "name": "Admin",
    "role": "admin"
  }
}
```

---

### Projects (`/api/v1/projects/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | List all projects | Public |
| POST | `/` | Create project | Admin |
| GET | `/{id}/` | Get project details | Public |
| PUT | `/{id}/` | Update project | Admin |
| PATCH | `/{id}/` | Partial update | Admin |
| DELETE | `/{id}/` | Delete project | Admin |

---

### Services (`/api/v1/services/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | List all services | Public |
| POST | `/` | Create service | Admin |
| GET | `/{id}/` | Get service details | Public |
| PUT | `/{id}/` | Update service | Admin |
| DELETE | `/{id}/` | Delete service | Admin |

---

### Blogs (`/api/v1/blogs/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | List all blogs | Public |
| POST | `/` | Create blog post | Admin |
| GET | `/{id}/` | Get blog by ID | Public |
| GET | `/slug/{slug}/` | Get blog by slug | Public |
| PUT | `/{id}/` | Update blog | Admin |
| DELETE | `/{id}/` | Delete blog | Admin |

---

### Messages (`/api/v1/messages/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/` | Send message | Public |
| GET | `/` | List all messages | Admin |
| PUT | `/{id}/read/` | Mark as read | Admin |

---

### Settings (`/api/v1/settings/`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | Get site settings | Public |
| PUT | `/` | Update site settings | Admin |

---

## Authentication & Authorization

### JWT Configuration

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Permission Levels

1. **Public:** No authentication required (GET endpoints for projects, services, blogs, settings)
2. **Authenticated:** Valid JWT token required (user profile, logout)
3. **Admin:** User with `role='admin'` required (all create/update/delete operations)

### Using JWT in Requests

```bash
# Include in headers
Authorization: Bearer <access_token>
```

---

## Deployment Configuration

### Environment Variables (`.env`)

```env
DEBUG=True
SECRET_KEY=django-insecure-change-me-in-production

# PostgreSQL (Optional - Currently using SQLite)
# DB_NAME=DigitalCoreProduction
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
```

### Database Configuration

**Current:** SQLite (development)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**PostgreSQL Ready:** See `DATABASE_SWITCHING_GUIDE.md`

### Production Hosts

```python
ALLOWED_HOSTS = [
    'digitalcorebackend.onrender.com',
    'www.digitalcorebackend.onrender.com',
]
```

### Static Files

- **URL:** `/static/`
- **Storage:** WhiteNoise with compression
- **Media:** `/media/` for user uploads

### Build Script (`build.sh`)

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
```

---

## Development Setup

### 1. Clone & Install

```bash
git clone <repository-url>
cd WeboraBackend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create .env file with configuration
DEBUG=True
SECRET_KEY=your-secret-key
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Seed Initial Data

```bash
python seed_data.py
```

**Creates:**
- Admin user: `admin@digitalcore.com` / `admin123`
- Sample site settings
- Sample service, project, and blog

### 5. Run Development Server

```bash
python manage.py runserver
```

Access at: `http://localhost:8000`

### 6. Admin Panel

Access Django admin: `http://localhost:8000/admin/`

---

## Key Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| **JWT Authentication** | ✅ Complete | Email-based login with JWT tokens |
| **Role-Based Access** | ✅ Complete | Admin/User permissions |
| **Projects CRUD** | ✅ Complete | Portfolio management with images |
| **Services CRUD** | ✅ Complete | Service offerings catalog |
| **Blog System** | ✅ Complete | Slug-based blog with images |
| **Contact Forms** | ✅ Complete | Message handling system |
| **Site Settings** | ✅ Complete | Global configuration singleton |
| **Image Uploads** | ✅ Complete | Projects & blogs support images |
| **CORS Support** | ✅ Complete | Frontend integration ready |
| **Production Ready** | ✅ Complete | Gunicorn + WhiteNoise configured |
| **Database Flexibility** | ✅ Complete | SQLite/PostgreSQL support |
| **Environment Config** | ✅ Complete | .env based configuration |
| **Seed Data** | ✅ Complete | Quick setup with sample data |
| **API Versioning** | ✅ Complete | All endpoints under /api/v1/ |

---

## Version History

### v1.0.0 (Current)
- ✅ Complete authentication system with JWT
- ✅ Projects, Services, Blogs, Contacts, Settings modules
- ✅ Image upload support
- ✅ Role-based permissions
- ✅ Production deployment configuration
- ✅ Database migration guide
- ✅ Rebranded to DigitalCore Solutions
- ✅ SQLite as default (PostgreSQL ready)

---

## Future Enhancements (Planned)

- [ ] Email integration for OTP verification
- [ ] Password reset functionality
- [ ] Advanced filtering and search
- [ ] Pagination for large datasets
- [ ] Rate limiting
- [ ] API documentation (Swagger/ReDoc)
- [ ] Automated testing suite
- [ ] File upload size validation
- [ ] Admin analytics dashboard
- [ ] Multi-language support

---

## Documentation Files

- **README.md** - Quick start guide
- **DATABASE_SWITCHING_GUIDE.md** - PostgreSQL migration guide
- **VERSION_IMPLEMENTATION_PLAN.md** - This file (complete feature overview)

---

## Contact & Support

**Project:** DigitalCore Solutions Backend  
**Email:** info@digitalcoresolutions.com  
**Repository:** GitHub/DigitalCore  

---

*Last Updated: January 29, 2026*  
*Version: 1.0.0*  
*Status: Production Ready ✅*
