Social Media API
A RESTful Social Media API built with Django and Django REST Framework.

The project currently provides user registration, token-based authentication, and authenticated profile management.

Features
User registration
User login
Token-based authentication
Authenticated profile retrieval
Authenticated profile updates
Custom user model
User bio
Profile pictures
Followers and following relationships
Django admin interface
SQLite database for development
Technologies
Python
Django 4.2
Django REST Framework
Django REST Framework Token Authentication
SQLite
Project Structure
social_media_api/
├── manage.py
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── db.sqlite3
