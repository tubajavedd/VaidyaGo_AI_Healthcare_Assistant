import os
import django
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaidyaGo.settings')
django.setup()

from AdminLogin.models import User
from Dr_personalInfo.models import DoctorPersonalInfo

print(f"Total Users: {User.objects.count()}")
print(f"Total Doctors (User model): {User.objects.filter(role='DOCTOR').count()}")
print(f"Total DoctorPersonalInfo records: {DoctorPersonalInfo.objects.count()}")

for dp in DoctorPersonalInfo.objects.all():
    print(f"DP ID: {dp.id}, Name: {dp.first_name} {dp.last_name}, Status: {dp.status}")

for user in User.objects.filter(role='DOCTOR'):
    print(f"User: {user.username}, Email: {user.email}")
