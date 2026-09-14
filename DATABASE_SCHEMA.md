# Database Schema

## User

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| username | Varchar |
| email | Varchar |
| role | Varchar |
| phone_number | Varchar |
| address | Text |
| email_verified | Boolean |

---

## Department

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| name | Varchar |
| description | Text |
| head_id | Integer (FK) |

---

## Doctor

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| user_id | Integer (FK) |
| department_id | Integer (FK) |
| specialization | Varchar |
| license_number | Varchar |
| years_of_experience | Integer |
| consultation_fee | Decimal |

---

## Patient

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| user_id | Integer (FK) |
| date_of_birth | Date |
| gender | Varchar |
| blood_group | Varchar |

---

## Appointment

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| patient_id | Integer (FK) |
| doctor_id | Integer (FK) |
| appointment_date | DateTime |
| status | Varchar |

---

## MedicalRecord

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| patient_id | Integer (FK) |
| doctor_id | Integer (FK) |
| diagnosis | Text |

---

## Prescription

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| medical_record_id | Integer (FK) |
| medication_name | Varchar |

---

## LaboratoryRequest

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| patient_id | Integer (FK) |
| doctor_id | Integer (FK) |
| test_name | Varchar |

---

## LaboratoryResult

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| laboratory_request_id | Integer (FK) |

---

## Invoice

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| patient_id | Integer (FK) |
| total_amount | Decimal |

---

## Payment

| Field | Type |
|---------|---------|
| id | Integer (PK) |
| invoice_id | Integer (FK) |
| patient_id | Integer (FK) |
| amount | Decimal |

---

## Relationships

- User ↔ Doctor (One-to-One)
- User ↔ Patient (One-to-One)
- Department ↔ Doctor (One-to-Many)
- Patient ↔ Appointment (One-to-Many)
- Doctor ↔ Appointment (One-to-Many)
- Patient ↔ MedicalRecord (One-to-Many)
- Doctor ↔ MedicalRecord (One-to-Many)
- MedicalRecord ↔ Prescription (One-to-Many)
- Patient ↔ LaboratoryRequest (One-to-Many)
- Doctor ↔ LaboratoryRequest (One-to-Many)
- LaboratoryRequest ↔ LaboratoryResult (One-to-One)
- Patient ↔ Invoice (One-to-Many)
- Invoice ↔ Payment (One-to-Many)