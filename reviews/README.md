# Healthcare Management System API

## Project Overview

The Healthcare Management System is a backend RESTful API built with Django and Django REST Framework (DRF). It enables hospitals, clinics, and healthcare providers to manage patients, doctors, appointments, medical records, prescriptions, laboratory requests, billing, and healthcare services through secure REST APIs.

## Features

* JWT Authentication
* Department Management
* Doctor Management
* Patient Management
* Appointment Scheduling
* Medical Records Management
* Prescription Management
* Laboratory Management
* Billing and Payments
* API Documentation with Swagger

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* Simple JWT
* drf-spectacular

## Installation

1. Clone the repository

```bash
git clone <repository-url>
cd healthcare_management_system
```

2. Create and activate a virtual environment

```bash
python -m venv venv
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Apply migrations

```bash
python manage.py migrate
```

5. Run the development server

```bash
python manage.py runserver
```

## API Documentation

Swagger Documentation:

```text
http://127.0.0.1:8000/api/docs/
```

## Authentication

The API uses JWT Authentication.

Available endpoints:

* Register
* Login
* Token Refresh

## Main Modules

* Accounts
* Departments
* Doctors
* Patients
* Appointments
* Medical Records
* Prescriptions
* Laboratory
* Billing

## Author

Adeyemi Ifeoluwa
