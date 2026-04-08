import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_website.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile

users_without_profile = User.objects.filter(profile__isnull=True)
count = users_without_profile.count()
print(f"Found {count} users without a profile.")

for user in users_without_profile:
    Profile.objects.create(user=user)
    print(f"Created profile for {user.username}")

print("Done.")
