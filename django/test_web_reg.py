import requests

url = "http://127.0.0.1:8000/accounts/register/"

res = requests.get(url)
csrf = res.cookies['csrftoken']

data = {
    'csrfmiddlewaretoken': csrf,
    'username': 'test_curl_user2',
    'password': 'Password123',
    'password_confirm': 'Password123',
    'email': 'test2@test.com',
    'first_name': 'Test',
    'last_name': 'User',
    'phone': '111222333'
}

post_res = requests.post(url, data=data, cookies=res.cookies)
print("Status:", post_res.status_code)
