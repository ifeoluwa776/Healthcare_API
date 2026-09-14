# Healthcare Management System API

A backend RESTful API built with Django and Django REST Framework (DRF) for managing healthcare operations.

## Project Overview

The Healthcare Management System enables hospitals, clinics, and healthcare providers to manage patients, doctors, appointments, medical records, prescriptions, laboratory services, billing, notifications, reviews, and analytics through secure REST APIs.

## Features

* JWT authentication
* User registration and login
* Token refresh and logout
* Email verification
* Password reset
* Role-based access control
* Department management
* Doctor management
* Doctor license uploads
* Doctor profile photo uploads
* Patient management
* Patient genotype and medical profile
* Appointment scheduling
* Appointment status management
* Appointment reminders
* Medical records management
* Medical record file attachments
* Prescription management
* Prescription download
* Laboratory requests and results
* Laboratory report uploads and downloads
* Billing and payments
* Payment receipt generation
* Notifications
* Email notifications
* Doctor reviews and ratings
* Doctor average ratings
* Admin analytics
* Search and filtering
* API pagination
* Request throttling
* Swagger/OpenAPI documentation
* Postman API collection
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

Appointment reminders are available through:

* `/api/appointments/{id}/remind/`

### Medical Records

* `/api/medical-records/`

### Prescriptions

* `/api/prescriptions/`

Prescription downloads are available through:

* `/api/prescriptions/{id}/download/`

### Laboratory

* `/api/laboratory/requests/`
* `/api/laboratory/results/`

Laboratory report downloads are available through:

* `/api/laboratory/results/{id}/download/`

### Billing

* `/api/billing/invoices/`
* `/api/billing/payments/`
* `/api/billing/payments/{payment_id}/receipt/`

### Notifications

* `/api/notifications/`

### Reviews

* `/api/reviews/`

Doctor average ratings are available through the reviews API.

### Analytics
