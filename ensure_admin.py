import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
sys.path.insert(0, str(Path(__file__).parent))
django.setup()

from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def ensure_admin():
    admin_email = getattr(settings, "ADMIN_EMAIL", "khanadiba9746@gmail.com")
    admin_username = "admin_khanadiba"
    admin_password = "admin_password123" # User should change this later

    user, created = User.objects.get_or_create(
        email=admin_email,
        defaults={
            'username': admin_username,
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True,
        }
    )

    if created:
        user.set_password(admin_password)
        user.save()
        print(f"Admin user created: {admin_email}")
        print(f"Initial Password: {admin_password}")
    else:
        # Ensure existing user has admin rights
        user.role = 'ADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"Admin user already exists: {admin_email}. Admin rights ensured.")

if __name__ == '__main__':
    ensure_admin()
