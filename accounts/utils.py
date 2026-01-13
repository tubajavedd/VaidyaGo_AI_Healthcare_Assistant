import re
import random
import string
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_username_from_email(email):
    # 1. take text before @
    base = email.split('@')[0]

    # 2. remove special characters
    base = re.sub(r'[^a-zA-Z0-9]', '', base)

    # 3. ensure minimum length
    if len(base) < 6:
        base += ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    # 4. take first 6 characters
    username = base[:6]

    # 5. make sure username is unique
    while User.objects.filter(username=username).exists():
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    return username
