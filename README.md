# Healthcare Management System API

A backend RESTful API built with Django and Django REST Framework (DRF) for managing healthcare operations.

## Project Overview

The Healthcare Management System enables hospitals, clinics, and healthcare providers to manage patients, doctors, appointments, medical records, prescriptions, laboratory services, billing, notifications, and reviews through secure REST APIs.

## Features

* JWT authentication
* User registration and login
* Token refresh and logout
* Role-based access control
* Department management
* Doctor management
* Patient management
* Appointment scheduling
* Medical records management
* Prescription management
* Laboratory requests and results
* Billing and payments
* Payment receipt generation
* Notifications
* Doctor reviews and ratings
* Admin analytics
* Search and filtering
* API pagination
* Doctor profile photo uploads
* Request throttling
* Swagger/OpenAPI documentation
* Automated tests

## User Roles

The system supports:

* Admin
* Doctor
* Nurse
* Receptionist
* Laboratory Technician
* Patient

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* Simple JWT
* Django Filters
* drf-spectacular
* django-cors-headers

## API Documentation

Swagger documentation:

`http://127.0.0.1:8000/api/docs/`

OpenAPI schema:

`http://127.0.0.1:8000/api/schema/`

## Main API Endpoints

### Authentication

* `/api/accounts/register/`
* `/api/accounts/login/`
* `/api/accounts/refresh/`
* `/api/accounts/profile/`
* `/api/accounts/logout/`
* `/api/accounts/reset-password/`
* `/api/accounts/verify-email/`

### Departments

* `/api/departments/`

### Doctors

* `/api/doctors/`

### Patients

* `/api/patients/`

### Appointments

* `/api/appointments/`

### Medical Records

* `/api/medical-records/`

### Prescriptions

* `/api/prescriptions/`

### Laboratory

* `/api/laboratory/requests/`
* `/api/laboratory/results/`

### Billing

* `/api/billing/invoices/`
* `/api/billing/payments/`
* `/api/billing/payments/{payment_id}/receipt/`

### Notifications

* `/api/notifications/`

### Reviews

* `/api/reviews/`

### Analytics

* `/api/analytics/`

## Running the Project

### 1. Clone or download the project

Open the project folder in your terminal.

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an admin account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

## Running Tests

Run the complete test suite with:

```bash
python manage.py test
```

The current test suite contains **56 automated tests**, covering authentication, permissions, CRUD operations, appointments, patients, doctors, medical records, prescriptions, laboratory services, billing, notifications, reviews, search/filtering, analytics, and file uploads.

## API Testing

The API can be tested using:

* Swagger/OpenAPI documentation
* Postman

Swagger:

`http://127.0.0.1:8000/api/docs/`

A Postman collection is also available for testing the API endpoints.

## Database

The project uses SQLite for database storage during development.

The database contains models for:

* Users
* Departments
* Doctors
* Patients
* Appointments
* Medical Records
* Prescriptions
* Laboratory Requests
* Laboratory Results
* Invoices
* Payments
* Notifications
* Reviews

## Authentication

The API uses JSON Web Tokens (JWT) for authentication.

After logging in, the access token should be supplied in the request header:

```text
Authorization: Bearer <access_token>
```

The refresh endpoint can be used to obtain a new access token when required.

## File Uploads

Doctor profile photos and laboratory reports can be uploaded through the relevant APIs.

Uploaded media files are served during development using Django's media configuration.

## Project Documentation

The project includes:

* Source code
* README documentation
* ER diagram
* Database schema
* Swagger/OpenAPI documentation
* Postman collection
* Automated test cases

## Project Status

The Healthcare Management System API has been implemented with authentication, role-based permissions, healthcare management modules, API documentation, file upload support, search/filtering, analytics, and automated testing.
