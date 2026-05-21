## How the Social Media API Works

This API is built with **Django** and **Django REST Framework (DRF)** and focuses on user authentication and profiles.

### 1. Custom User Model

A custom user model extends Django’s default user to add:

* bio
* profile picture
* followers (users can follow each other)

This allows basic social media functionality.

---

### 2. Authentication (Token-Based)

When a user registers or logs in, the system generates a **token**.

* The token is returned to the user
* It is used to identify the user in future requests

Each protected request includes:

```http
Authorization: Token <user_token>
```

---

### 3. Main API Flow

* **Register** → creates user + returns token
* **Login** → verifies user + returns token
* **Profile** → requires token to view or update user data

---

### 4. How It Works Internally

* Django stores user data in the database
* DRF checks the token on every request
* If valid → user is authenticated
* If not → access is denied

---

### Summary

The system works by using **tokens as user identity**, allowing secure registration, login, and profile management through simple API endpoints.
