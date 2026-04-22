import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_website.settings")
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile

username = "test_reg_user"
phone = "1234567890"
user = User.objects.create_user(username=username, password="123")
profile, created = Profile.objects.get_or_create(user=user)
profile.phone = phone
profile.save()

p = Profile.objects.get(user__username=username)
print("Saved phone:", p.phone)
