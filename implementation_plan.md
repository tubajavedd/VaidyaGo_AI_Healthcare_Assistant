# Implementation Plan - Restrict Admin Access

The goal is to restrict admin privileges to a single user (`khanadiba9746@gmail.com`), remove the ability for anyone else to sign up as an admin, and ensure this specific user is pre-configured in the system for direct login.

## User Review Required
> [!IMPORTANT]
> This change will hardcode the admin email. Ensure `khanadiba9746@gmail.com` is the correct and only intended admin.
>
> **Direct Feed**: I will provide an `ensure_admin.py` script to create the admin user with a default password. You will need to run this once.

## Proposed Changes

### Settings Configuration

#### [MODIFY] [settings.py](file:///d:/directory/vaidyaGo/vaidyaGo/vaidyaGo/settings.py)
- Set `ALLOW_ADMIN_SIGNUP = False`.
- Add `ADMIN_EMAIL = "khanadiba9746@gmail.com"`.

### Authentication & Authorization Logic

#### [MODIFY] [views.py](file:///d:/directory/vaidyaGo/vaidyaGo/AdminLogin/views.py)
- **`admin_signup`**: Update to strictly block any signup where `usertype == "admin"`.
- **`AdminLoginView`**: Update the `post` method. If the logging-in user's email is `khanadiba9746@gmail.com`, explicitly set `role = "ADMIN"`, `is_staff = True`, and `is_superuser = True` in the response and JWT claims.

#### [MODIFY] [serializers.py](file:///d:/directory/vaidyaGo/vaidyaGo/AdminLogin/serializers.py)
- **`AdminSignupSerializer.validate_usertype`**: Update to disallow `"admin"` usertype during signup.

#### [MODIFY] [permissions.py](file:///d:/directory/vaidyaGo/vaidyaGo/AdminLogin/permissions.py)
- **`IsAdmin`**: Update `has_permission` to explicitly allow access if `user.email == settings.ADMIN_EMAIL`.

### Data Migration / Scripting

#### [NEW] [ensure_admin.py](file:///d:/directory/vaidyaGo/vaidyaGo/ensure_admin.py)
- A standalone script to ensure `khanadiba9746@gmail.com` exists in the database with the `ADMIN` role and necessary flags.

## Verification Plan

### Automated Tests
- Attempt admin signup (should fail).
- Login with `khanadiba9746@gmail.com` and verify admin role in token.
