# Database Schema

## User

| Field          | Type         |
| -------------- | ------------ |
| id             | Integer (PK) |
| username       | Varchar      |
| email          | Varchar      |
| role           | Varchar      |
| phone_number   | Varchar      |
| address        | Text         |
| email_verified | Boolean      |

---

## Department

| Field       | Type                   |
| ----------- | ---------------------- |
| id          | Integer (PK)           |
| name        | Varchar                |
| description | Text                   |
| head_id     | Integer (FK, nullable) |

---

## Doctor

| Field               | Type                     |
| ------------------- | ------------------------ |
| id                  | Integer (PK)             |
| user_id             | Integer (FK, One-to-One) |
| department_id       | Integer (FK)             |
| specialization      | Varchar                  |
| license_number      | Varchar, Unique          |
| years_of_experience | Integer                  |
| consultation_fee    | Decimal                  |
| availability        | JSON                     |
| profile_photo       | Image/File, nullable     |

---

## Patient

| Field              | Type                     |
| ------------------ | ------------------------ |
| id                 | Integer (PK)             |
| user_id            | Integer (FK, One-to-One) |
| date_of_birth      | Date                     |
| gender             | Varchar                  |
| blood_group        | Varchar                  |
| address            | Text                     |
| emergency_contact  | JSON                     |
| insurance_provider | Varchar                  |
| insurance_details  | Text                     |
| allergies          | Text                     |

---

## Appointment

| Field            | Type         |
| ---------------- | ------------ |
| id               | Integer (PK) |
| patient_id       | Integer (FK) |
| doctor_id        | Integer (FK) |
| appointment_date | DateTime     |
| status           | Varchar      |
| reason           | Text         |
| created_at       | DateTime     |

### Appointment Statuses

* Pending
* Approved
* Completed
* Cancelled
* Missed

---

## MedicalRecord

| Field              | Type         |
| ------------------ | ------------ |
| id                 | Integer (PK) |
| patient_id         | Integer (FK) |
| doctor_id          | Integer (FK) |
| diagnosis          | Text         |
| symptoms           | Text         |
| treatment          | Text         |
| consultation_notes | Text         |
| visit_date         | DateTime     |

---

## Prescription

| Field             | Type         |
| ----------------- | ------------ |
| id                | Integer (PK) |
| medical_record_id | Integer (FK) |
| medication_name   | Varchar      |
| dosage            | Varchar      |
| instructions      | Text         |
| created_at        | DateTime     |

---

## LaboratoryRequest

| Field                    | Type                   |
| ------------------------ | ---------------------- |
| id                       | Integer (PK)           |
| patient_id               | Integer (FK)           |
| doctor_id                | Integer (FK)           |
| laboratory_technician_id | Integer (FK, nullable) |
| test_name                | Varchar                |
| description              | Text                   |
| status                   | Varchar                |
| requested_at             | DateTime               |

### Laboratory Request Statuses

* Requested
* Sample Collected
* In Progress
* Completed
* Cancelled

---

## LaboratoryResult

| Field                 | Type                     |
| --------------------- | ------------------------ |
| id                    | Integer (PK)             |
| laboratory_request_id | Integer (FK, One-to-One) |
| result                | Text                     |
| notes                 | Text                     |
| report                | File, nullable           |
| completed_at          | DateTime                 |

---

## Invoice

| Field              | Type         |
| ------------------ | ------------ |
| id                 | Integer (PK) |
| patient_id         | Integer (FK) |
| consultation_fee   | Decimal      |
| laboratory_charges | Decimal      |
| medication_charges | Decimal      |
| total_amount       | Decimal      |
| status             | Varchar      |
| created_at         | DateTime     |

### Invoice Statuses

* Pending
* Paid
* Failed
* Refunded

---

## Payment

| Field          | Type              |
| -------------- | ----------------- |
| id             | Integer (PK)      |
| invoice_id     | Integer (FK)      |
| patient_id     | Integer (FK)      |
| amount         | Decimal           |
| payment_method | Varchar           |
| status         | Varchar           |
| transaction_id | Varchar, nullable |
| paid_at        | DateTime          |

### Payment Methods

* Cash
* Card
* Bank Transfer
* Online Payment

### Payment Statuses

* Pending
* Paid
* Failed
* Refunded

---

## Notification

| Field             | Type         |
| ----------------- | ------------ |
| id                | Integer (PK) |
| user_id           | Integer (FK) |
| title             | Varchar      |
| message           | Text         |
| notification_type | Varchar      |
| is_read           | Boolean      |
| created_at        | DateTime     |

### Notification Types

* Appointment
* Prescription
* Laboratory
* Billing
* General

---

## Review

| Field      | Type         |
| ---------- | ------------ |
| id         | Integer (PK) |
| patient_id | Integer (FK) |
| doctor_id  | Integer (FK) |
| rating     | Integer      |
| feedback   | Text         |
| created_at | DateTime     |

---

## Relationships

* User ↔ Doctor (One-to-One)
* User ↔ Patient (One-to-One)
* User ↔ LaboratoryRequest (One-to-Many, laboratory technician assignment)
* User ↔ Notification (One-to-Many)
* Department ↔ Doctor (One-to-Many)
* Department ↔ Doctor as Head (One-to-One/Optional)
* Patient ↔ Appointment (One-to-Many)
* Doctor ↔ Appointment (One-to-Many)
* Patient ↔ MedicalRecord (One-to-Many)
* Doctor ↔ MedicalRecord (One-to-Many)
* MedicalRecord ↔ Prescription (One-to-Many)
* Patient ↔ LaboratoryRequest (One-to-Many)
* Doctor ↔ LaboratoryRequest (One-to-Many)
* LaboratoryRequest ↔ LaboratoryResult (One-to-One)
* Patient ↔ Invoice (One-to-Many)
* Invoice ↔ Payment (One-to-Many)
* Patient ↔ Payment (One-to-Many)
* Patient ↔ Review (One-to-Many)
* Doctor ↔ Review (One-to-Many)
