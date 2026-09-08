Social Media API
A RESTful Social Media API built with Django and Django REST Framework (DRF).

The API provides user authentication, profiles, follow/follower relationships, posts, comments, search, pagination, and author-based permissions.

✨ Features

Authentication & Users

User registration
User login
Token-based authentication
Custom user model
Authenticated profile retrieval
Authenticated profile updates
User bio
Profile pictures

Follow System

Follow other users
Unfollow users
Prevent users from following themselves
View users you are following
View your followers
View another user's following list
View another user's followers
Follower and following counts
Users can only modify their own following relationships

Posts

Create posts
View posts
Update your own posts
Delete your own posts
Posts ordered by creation date, newest first
Search posts by title and content
Automatic assignment of post author
Pagination

Comments

Create comments
View comments
Update your own comments
Delete your own comments
Filter comments by post
Comments ordered by creation date, newest first
Automatic assignment of comment author
Pagination

Permissions

Authentication required for protected endpoints
Users can modify only their own posts
Users can modify only their own comments
Users cannot modify another user's posts or comments
Following relationships are managed through dedicated follow/unfollow endpoints
Administration & Database
Django admin interface
SQLite database for development

🛠️ Technologies

Python
Django 4.2
Django REST Framework
DRF Token Authentication
SQLite

📁 Project Structure

social_media_api/
│
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
├── posts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── pagination.py
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
