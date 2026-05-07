import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def check_users():
    count = User.objects.count()
    print(f"Total users: {count}")
    if count > 0:
        for user in User.objects.all():
            print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}")

if __name__ == "__main__":
    check_users()
