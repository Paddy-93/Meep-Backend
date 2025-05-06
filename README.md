# Meep – Backend (Django + REST Framework)

## Tech Stack

- Python 3
- Django 4
- Django REST Framework
- SQLite (for development)
- PostgreSQL (for production)

## Project Setup

### 1. Create a virtual environment

    python3 -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Run database migrations

    python manage.py makemigrations
    python manage.py migrate

### 4. Start the development server

    python manage.py runserver

To test from a mobile device:

    python manage.py runserver 0.0.0.0:8000

## Admin Access

To create an admin user:

    python manage.py createsuperuser

Then open:

    http://localhost:8000/admin/

## API Endpoints

    GET  /jobs/     - List all jobs
    POST /jobs/     - Create a new job

## PostgreSQL Setup (Optional)

To use PostgreSQL instead of SQLite:

1.  Install PostgreSQL
2.  Update the `DATABASES` config in `backend/settings.py`:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'your_db_name',
                'USER': 'your_db_user',
                'PASSWORD': 'your_db_password',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }

3.  Install the Postgres driver:

        pip install psycopg2-binary

4.  Run migrations again:

        python manage.py migrate
