# Fix Visibility of Registered and Pending Doctors in Admin Approval

Admins cannot see doctors in the "Approval Section" in two cases:
1. When a doctor has registered (User account created) but hasn't filled the Personal Information form yet.
2. When a doctor has started the process (status 'incomplete') but hasn't reached 'pending' status yet.

This plan ensures both types of doctors are visible to the admin.

## User Review Required

> [!NOTE]
> Doctors who have only registered (User account only) will be displayed with their username/email and a status of "New Registration". Admins can see them, but full approval will still require them to submit their profile details.

## Proposed Changes

### Backend (Admin API)

#### [MODIFY] [views.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/AdminLogin/views.py)
- Update `pending_doctors` view to:
    - Include `DoctorPersonalInfo` with status `pending` or `incomplete`.
    - Include `User` accounts with role `DOCTOR` that have no corresponding `DoctorPersonalInfo` record.
    - Provide `specialization` and `experience` fields (using data from `DoctorProfessionalInfo` if available).

#### [MODIFY] [tool_router.py](file:///d:/directory/UPDATED_VAIDYAGO/vaidyaGo/vaidyaGo/chatbot_admin/services/tool_router.py)
- Update `_list_pending_doctors` tool to follow the same logic as the main API (including new registrations).

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
