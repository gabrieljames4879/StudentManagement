# EduQuantra Student Management System (Django)

## Quick Setup & Sample Data Seeding
1. Install Django:
   `pip install django`
2. Run database migrations:
   `python manage.py makemigrations`
   `python manage.py migrate`
3. Seed sample students & demo admin account (`admin` / `admin12345`):
   `python manage.py seed_students`
4. Start the server:
   `python manage.py runserver`
5. Open http://127.0.0.1:8000/ and log in with `admin` / `admin12345`.
