# Walkthrough - Fix 403 Forbidden on Doctor Approval

I have implemented the fixes to resolve the 403 Forbidden error encountered when approving doctors.

## Changes Made

### 1. Unified REST Framework Settings
In `vaidyaGo/settings.py`, I merged the two separate `REST_FRAMEWORK` dictionary definitions. This prevents the second definition from overwriting the first, ensuring that `DEFAULT_PERMISSION_CLASSES` (which requires authentication) and `DEFAULT_AUTHENTICATION_CLASSES` (which handles Sessions, Tokens, and JWT) are both active.

### 2. Updated Permission Logic
In `AdminLogin/views.py`, I updated the following views to use the project's custom `IsAdmin` permission class instead of the built-in `IsAdminUser`:
- `pending_doctors`
- `approve_doctor`
- `reject_doctor`

The `IsAdmin` class specifically checks for the `role == "ADMIN"` attribute on your custom User model, which is more reliable and consistent with the rest of your application's access control.

## Verification
Please retry the doctor approval action in your browser or API client.
1. Ensure you are logged in as an Admin.
2. Send a POST request to `/accounts/doctors/approve/<doctor_id>/`.
3. It should now return a `200 OK` (Doctor approved) instead of a `403 Forbidden`.
