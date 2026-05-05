# Implementation Plan - Fix 403 Forbidden on Doctor Approval

The user is encountering a `403 Forbidden` error when trying to approve a doctor via the POST endpoint `/accounts/doctors/approve/<int:doctor_id>/`.

## Analysis of the Issue

1.  **Redundant Settings**: `vaidyaGo/settings.py` has two `REST_FRAMEWORK` definitions. The second one overwrites the first, losing the `DEFAULT_PERMISSION_CLASSES`.
2.  **Permission Discrepancy**: The `approve_doctor` view uses `IsAdminUser` (checks `is_staff`), while the project's custom logic uses `IsAdmin` (checks `role == "ADMIN"`).
3.  **CSRF/Auth**: `SessionAuthentication` is enabled, which might cause CSRF issues if not handled, but fixing the permission class is the primary architectural fix.

## Proposed Changes

### 1. `vaidyaGo/settings.py`
- Merge `REST_FRAMEWORK` settings into a single block.

### 2. `AdminLogin/views.py`
- Switch from `IsAdminUser` to `IsAdmin` in `pending_doctors`, `approve_doctor`, and `reject_doctor`.

## Verification Plan
- User to verify by retrying the approval action.
