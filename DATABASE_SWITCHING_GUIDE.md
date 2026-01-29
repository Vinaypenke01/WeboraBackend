# Database Switching Guide

This guide explains how to switch between SQLite and PostgreSQL databases in the WeboraBackend project.

## Current Configuration: SQLite

The project currently uses **SQLite** as the database backend. This is suitable for:
- Local development
- Small to medium-sized applications
- Quick prototyping
- Projects without concurrent write requirements

---

## Switching from SQLite to PostgreSQL

Follow these steps when you're ready to migrate to PostgreSQL:

### Step 1: Install PostgreSQL

**Windows:**
1. Download PostgreSQL from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Install PostgreSQL and remember your password
3. Default port is `5432`

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

---

### Step 2: Create PostgreSQL Database

Open PostgreSQL command line (psql) and run:

```sql
CREATE DATABASE WeboraProduction;
CREATE USER postgres WITH PASSWORD '123456';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE WeboraProduction TO postgres;
```

Or use pgAdmin GUI tool to create the database.

---

### Step 3: Update Environment Variables

Edit your `.env` file with your PostgreSQL credentials:

```env
DEBUG=True
SECRET_KEY=django-insecure-change-me-in-production

# PostgreSQL Configuration
DB_NAME=WeboraProduction
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

---

### Step 4: Install PostgreSQL Python Driver

The `psycopg2-binary` package is already in `requirements.txt`. If needed, install it:

```bash
pip install psycopg2-binary
```

---

### Step 5: Update settings.py

Open `config/settings.py` and make these changes:

**Comment out the SQLite configuration:**
```python
# SQLite Configuration (Currently Active)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```

**Uncomment the PostgreSQL configuration:**
```python
# PostgreSQL Configuration
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Render / Production with PostgreSQL
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Local PostgreSQL via .env
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
```

---

### Step 6: Migrate Your Data (Optional)

If you want to transfer existing SQLite data to PostgreSQL:

**Option A: Using Django's dumpdata/loaddata**

```bash
# Export data from SQLite
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > datadump.json

# Switch to PostgreSQL in settings.py

# Run migrations on PostgreSQL
python manage.py migrate

# Load data into PostgreSQL
python manage.py loaddata datadump.json
```

**Option B: Fresh Start**

```bash
# Simply run migrations on PostgreSQL (no data transfer)
python manage.py migrate

# Optionally seed initial data
python seed_data.py
```

---

### Step 7: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 8: Create Superuser (if fresh database)

```bash
python manage.py createsuperuser
```

---

## Switching Back to SQLite

If you need to switch back to SQLite:

1. **Comment out PostgreSQL configuration** in `config/settings.py`
2. **Uncomment SQLite configuration** in `config/settings.py`
3. Run migrations:
   ```bash
   python manage.py migrate
   ```

---

## Production Deployment (Render/Heroku)

For production environments using environment variables:

1. Set `DATABASE_URL` environment variable in your hosting platform
2. The code will automatically use PostgreSQL via `dj_database_url.parse()`
3. Example DATABASE_URL format:
   ```
   postgresql://username:password@hostname:5432/database_name
   ```

---

## Troubleshooting

### "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Connection refused
- Ensure PostgreSQL service is running
- Check if port 5432 is available
- Verify credentials in `.env` file

### Migration errors
```bash
# Reset migrations (WARNING: This deletes data)
python manage.py migrate --fake <app_name> zero
python manage.py migrate <app_name>
```

---

## Performance Comparison

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Setup Complexity | ⭐ Easy | ⭐⭐⭐ Moderate |
| Concurrent Writes | ❌ Limited | ✅ Excellent |
| Scalability | ⭐⭐ Small | ⭐⭐⭐⭐⭐ Large |
| Production Ready | ⚠️ Light use | ✅ Enterprise |
| Full-text Search | ⭐⭐ Basic | ⭐⭐⭐⭐⭐ Advanced |

---

## Recommendations

- **Use SQLite for:** Local development, prototyping, small projects
- **Use PostgreSQL for:** Production, multiple users, data integrity critical apps

---

## Need Help?

If you encounter issues during migration, check:
1. PostgreSQL service is running
2. Credentials in `.env` are correct
3. Database exists in PostgreSQL
4. `psycopg2-binary` is installed
