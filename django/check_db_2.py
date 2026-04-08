import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_website.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SHOW COLUMNS FROM accounts_profile")
    for row in cursor.fetchall():
        if row[2] == 'NO':  # Null is 'NO'
            print(row[0])
