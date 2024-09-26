# Simple-Inventory-Management


A Django REST framework-based inventory management API that supports CRUD operations with JWT authentication, Redis caching, and logging.

## Table of Contents
1. [Features](#features)
2. [Technologies](#technologies)
3. [Setup Instructions](#setup-instructions)
4. [API Endpoints](#api-endpoints)
5. [Usage Examples](#usage-examples)
6. [Logging](#logging)
7. [Running Unit Tests](#running-unit-tests)

## Features
- **CRUD Operations**: Create, read, update, and delete inventory items.
- **JWT Authentication**: Secure all endpoints.
- **Redis Caching**: Improve read performance by caching frequently accessed items.
- **Logging**: Log all significant events and errors for better monitoring and debugging.
- **PostgreSQL**: A robust and scalable database to store inventory data.
- **Unit Testing**: Unit tests to verify the functionality of all API endpoints.

## Technologies
- Python 3.8+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis
- JWT Authentication

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis


```bash
git clone https://github.com/yourusername/inventory-management-system.git
cd inventory-management-system

Set Up Virtual Environment
mkvirtualenv inventory

pip install -r requirements.txt

CREATE DATABASE inventory;

Update the .env file with your PostgreSQL credentials

Apply Migrations
python manage.py migrate

Create a Superuser
python manage.py createsuperuser

Run Redis Server
redis-server

Run the Django Server
python manage.py runserver



---API Endpoints---

Authentication

Register: POST /api/register/
Login: POST /api/login/
Refresh Token: POST /api/token/refresh/

Items

Create Item: POST /api/items/
Retrieve All Items: GET /api/items/
Retrieve Single Item: GET /api/items/<int:item_id>/
Update Item: PUT /api/items/<int:item_id>/
Delete Item: DELETE /api/items/<int:item_id>/



---Usage Examples---
User Registration -- curl -X POST http://127.0.0.1:8000/api/register/ -d '{"username": "newuser", "password": "password", "email": "user@example.com"}' -H "Content-Type: application/json"

User Login
curl -X POST http://127.0.0.1:8000/api/login/ -d '{"username": "newuser", "password": "password"}' -H "Content-Type: application/json"

Create Item
curl -X POST http://127.0.0.1:8000/api/items/ -d '{"name": "Item1", "description": "Description of Item1"}' -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json"

Retrieve Item
curl -X GET http://127.0.0.1:8000/api/items/1/ -H "Authorization: Bearer <access_token>"



---logging---
The application uses the Python logging module to log significant events and errors. Logs are stored in the logs/inventory.log file. To create the log file, you need to ensure the logs directory exists; the log file will be created automatically when the application runs.



---Running Unit Tests---
python manage.py test
