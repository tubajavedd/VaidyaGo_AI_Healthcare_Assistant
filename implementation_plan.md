# Fix Visibility of Registered and Pending Doctors in Admin Approval

<<<<<<< HEAD
The goal is to restrict admin privileges to a single user (`javedtuba1@gmail.com`), remove the ability for anyone else to sign up as an admin, and ensure this specific user is pre-configured in the system for direct login.

## User Review Required
> [!IMPORTANT]
> This change will hardcode the admin email. Ensure `javedtuba1@gmail.com` is the correct and only intended admin.
>
> **Direct Feed**: I will provide an `ensure_admin.py` script to create the admin user with a default password. You will need to run this once.
=======
Admins cannot see doctors in the "Approval Section" in two cases:
1. When a doctor has registered (User account created) but hasn't filled the Personal Information form yet.
2. When a doctor has started the process (status 'incomplete') but hasn't reached 'pending' status yet.

This plan ensures both types of doctors are visible to the admin.

## User Review Required

> [!NOTE]
> Doctors who have only registered (User account only) will be displayed with their username/email and a status of "New Registration". Admins can see them, but full approval will still require them to submit their profile details.
>>>>>>> main

## Proposed Changes

### Backend (Admin API)

<<<<<<< HEAD
#### [MODIFY] [settings.py](file:///d:/directory/vaidyaGo/vaidyaGo/vaidyaGo/settings.py)
- Set `ALLOW_ADMIN_SIGNUP = False`.
- Add `ADMIN_EMAIL = "javedtuba1@gmail.com"`.
=======
#### [MODIFY] [views.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/AdminLogin/views.py)
- Update `pending_doctors` view to:
    - Include `DoctorPersonalInfo` with status `pending` or `incomplete`.
    - Include `User` accounts with role `DOCTOR` that have no corresponding `DoctorPersonalInfo` record.
    - Provide `specialization` and `experience` fields (using data from `DoctorProfessionalInfo` if available).
>>>>>>> main

#### [MODIFY] [tool_router.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_admin/services/tool_router.py)
- Update `_list_pending_doctors` tool to follow the same logic as the main API (including new registrations).

<<<<<<< HEAD
#### [MODIFY] [views.py](file:///d:/directory/vaidyaGo/vaidyaGo/AdminLogin/views.py)
- **`admin_signup`**: Update to strictly block any signup where `usertype == "admin"`.
- **`AdminLoginView`**: Update the `post` method. If the logging-in user's email is `javedtuba1@gmail.com`, explicitly set `role = "ADMIN"`, `is_staff = True`, and `is_superuser = True` in the response and JWT claims.

#### [MODIFY] [serializers.py](file:///d:/directory/vaidyaGo/vaidyaGo/AdminLogin/serializers.py)
- **`AdminSignupSerializer.validate_usertype`**: Update to disallow `"admin"` usertype during signup.

#### [MODIFY] [permissions.py](file:///d:/directory/vaidyaGo/vaidyaGo/AdminLogin/permissions.py)
- **`IsAdmin`**: Update `has_permission` to explicitly allow access if `user.email == settings.ADMIN_EMAIL`.

### Data Migration / Scripting

#### [NEW] [ensure_admin.py](file:///d:/directory/vaidyaGo/vaidyaGo/ensure_admin.py)
- A standalone script to ensure `javedtuba1@gmail.com` exists in the database with the `ADMIN` role and necessary flags.

## Verification Plan

### Automated Tests
- Attempt admin signup (should fail).
- Login with `javedtuba1@gmail.com` and verify admin role in token.
=======
### Frontend (Admin Dashboard)

#### [MODIFY] [Admin_dashboard1.jsx](file:///d:/directory/UPDATED_VAIDYAGO/vaidyago_frontend/VaidyaGo/src/components/Admin/Admin_dashboard1.jsx)
- Update status display logic to show "Pending" for `pending`, `incomplete`, and `new_registration`.
- Ensure approval/rejection buttons are visible for these statuses.
- Handle cases where name or other details might be missing (fallback to username/email).

## Verification Plan

### Manual Verification
1. Create a new doctor account but do NOT fill the profile forms.
2. Log in as Admin and verify the doctor appears in the "Approval Section".
3. Fill the first profile form as the doctor and verify they still appear in the list.
4. Verify that the "Specialization" and "Experience" columns show actual data when available.
>>>>>>> main
