import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_website.settings")
django.setup()

from django.test import Client
from accounts.models import Profile
from django.contrib.auth.models import User

c = Client()
# Clean up previous test
User.objects.filter(username='test_flow_user').delete()

# 1. Register User
response = c.post('/accounts/register/', {
    'username': 'test_flow_user',
    'email': 'testflow@example.com',
    'password': 'Password123',
    'password_confirm': 'Password123',
    'first_name': 'Test',
    'last_name': 'Flow',
    'phone': '5558889999'
})

print("Registration Response Status:", response.status_code)
if response.status_code != 302:
    print("Registration Failed Context Form Errors:", response.context['form'].errors)

user = User.objects.get(username='test_flow_user')
print("Profile Phone after Registration:", user.profile.phone)

# 2. Login User
c.login(username='test_flow_user', password='Password123')

# 3. View Edit Profile Page
response2 = c.get('/accounts/edit-profile/')
print("Edit Profile Status:", response2.status_code)
content = response2.content.decode('utf-8')

if '5558889999' in content:
    print("SUCCESS: Phone number IS rendered in the edit profile HTML!")
else:
    print("ERROR: Phone number is NOT in the rendered HTML!")
