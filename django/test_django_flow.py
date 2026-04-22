import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linkStay.settings") # Wait, what is the settings module?
import sys
sys.path.append("/Users/gumjoseph/Desktop/link_stay/linkStay")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_website.settings")
django.setup()

from django.test import Client
from accounts.models import Profile
from django.contrib.auth.models import User

c = Client()
# Clean up previous test
User.objects.filter(username='test_flow_user2').delete()

# 1. Register User
response = c.post('/accounts/register/', {
    'username': 'test_flow_user2',
    'email': 'testflow@example.com',
    'password': 'Password123',
    'password_confirm': 'Password123',
    'first_name': 'Test',
    'last_name': 'Flow',
    'phone': '1234567890'
})

print("Registration Response Status:", response.status_code)
if response.status_code != 302:
    print("Registration Failed Context Form Errors:", getattr(response.context.get('form'), 'errors', 'No form in context'))

user = User.objects.get(username='test_flow_user2')
print("Profile Phone after Registration:", user.profile.phone)

# 2. Login User
c.login(username='test_flow_user2', password='Password123')

# 3. View Edit Profile Page
# Wait, user needs a booked hostel before they can view edit_profile?
# Let's check view logic!
EOF
