# Implementation Plan - Filter Medications "About to End"

The goal is to update the `/api/prescriptions/medications/` endpoint to return only those medicines that are "about to end" for the logged-in patient. This will help patients identify which prescriptions they need to renew.

## Proposed Changes

### Backend - Medication Views

#### [MODIFY] [newRequest_activePrescription_medication/views.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/newRequest_activePrescription_medication/views.py)
- Import `timezone`, `timedelta` from `datetime`.
- Import `PrescribedMedicine` from `prescription_management.models`.
- Update `MedicationListView` to:
    - Require authentication.
    - Filter medications based on the patient's `PrescribedMedicine` records.
    - A medicine is considered "about to end" if its calculated end date (`prescription_date + duration_days`) is within the next 7 days.

## Verification Plan

### Automated Tests
- None possible without live backend.

### Manual Verification
- Log in as a patient who has a prescribed medicine ending in 3 days.
- Access `http://127.0.0.1:8000/api/prescriptions/medications/`.
- Verify that only the expiring medicine is returned.
