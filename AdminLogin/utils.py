import re
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_username_from_email(email):
    # 1. take text before @
    base = email.split('@')[0]

    # 2. remove special characters
    base = re.sub(r'[^a-zA-Z0-9]', '', base) 

    # 3. ensure minimum length
    if len(base) < 6:
        base = base.ljust(6, '0')

    # 4. take first 6 characters
    base = base[:6]                                        #SLICING : [:6]
    username = base
    counter = 1

    # 5. ensure uniqueness WITHOUT randomness
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1

    return username
