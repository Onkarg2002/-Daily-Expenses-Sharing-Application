# Expense Sharing App Using Django & Django Rest Framework

## Overview

The Expense Sharing App is a web application built using Django and Django Rest Framework (DRF) that allows users to manage and track expenses shared among multiple participants. Users can create expenses, specify the amount and split method (equal, exact, or percentage), and view their expense history. The app also supports user registration, login, and downloading balance sheets.

## Features

- **User Management**: Users can register, log in, and manage their profiles.
- **Expense Tracking**: Create and track expenses with various split methods.
- **Participant Management**: Add participants to expenses and manage their shares.
- **Balance Sheets**: Download CSV reports of expenses and balances.
- **Admin Interface**: Manage users and expenses through Django’s admin interface.

## Technologies Used

- **Backend**: Django, Django Rest Framework (DRF)
- **Database**: SQLite (default), can be configured to use other databases
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Django’s built-in authentication system

## Installation

### Prerequisites

- Python 3.x
- Django 4.x
- Django Rest Framework (DRF)

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/expense-sharing-app.git
   cd expense-sharing-app

# To Run This Application 

# Create and Activate a Virtual Environment

python -m venv venv
venv\Scripts\activate

# Apply Migrations

python manage.py makemigrations
python manage.py migrate

# Create a Superuser

python manage.py createsuperuser

# For Run the server

python manage.py runserver


Access the app at http://127.0.0.1:8000/.

Usage
Accessing the Application
Home Page: Navigate to the home page to see an overview and navigation links.
Expense Management: Go to /expenses/add/ to add a new expense and /expenses/ to view existing expenses.
User Management: Access user registration and login pages via /register/ and /accounts/login/.
Admin Interface
To manage users and expenses, log in to the admin interface at /admin/ using the superuser credentials created during setup.

API Endpoints
User Management

GET /api/users/ - List all users
POST /api/users/ - Create a new user
Expense Management

GET /api/expenses/ - List all expenses
POST /api/expenses/ - Create a new expense
GET /api/expenses/{id}/ - Retrieve a specific expense
Balance Sheets

GET /api/expenses/balance_sheet/{user_id}/ - Download balance sheet for a specific user


