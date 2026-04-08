import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_website.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES")
    
    with open('db_out.txt', 'w') as f:
        f.write("TABLES:\n")
        for row in cursor.fetchall():
            if 'profile' in row[0] or 'user' in row[0] or 'auth' in row[0]:
                f.write("- " + row[0] + "\n")
        
        f.write("\nCOLUMNS in accounts_profile:\n")
        cursor.execute("SHOW COLUMNS FROM accounts_profile")
        for row in cursor.fetchall():
            f.write(str(row) + "\n")
