from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated users with ADMIN role.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        # Explicitly allow the configured admin email
        from django.conf import settings
        admin_email = getattr(settings, "ADMIN_EMAIL", None)
        if admin_email and user.email == admin_email:
            return True

        return getattr(user, "role", None) == "ADMIN"


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == "DOCTOR"
        )



class IsPatient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == "PATIENT"
        )
