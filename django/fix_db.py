import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_website.settings')
django.setup()

from django.db import connection

alter_queries = [
    "ALTER TABLE accounts_profile MODIFY bio longtext NULL;",
    "ALTER TABLE accounts_profile MODIFY sleep_schedule int NULL;",
    "ALTER TABLE accounts_profile MODIFY sleep_schedule_weight int NULL;",
    "ALTER TABLE accounts_profile MODIFY study_habit_weight int NULL;",
    "ALTER TABLE accounts_profile MODIFY cleanliness_weight int NULL;",
    "ALTER TABLE accounts_profile MODIFY social_activity int NULL;",
    "ALTER TABLE accounts_profile MODIFY social_activity_weight int NULL;",
    "ALTER TABLE accounts_profile MODIFY noise_tolerance int NULL;",
    "ALTER TABLE accounts_profile MODIFY noise_tolerance_weight int NULL;",
    "ALTER TABLE accounts_profile MODIFY smoking_status int NULL;",
    "ALTER TABLE accounts_profile MODIFY gender_preference int NULL;",
    "ALTER TABLE accounts_profile MODIFY gender_preference_weight int NULL;",
]

with connection.cursor() as cursor:
    for query in alter_queries:
        try:
            cursor.execute(query)
            print("Executed:", query)
        except Exception as e:
            print("Failed:", query, e)

print("Done. Extra columns in accounts_profile are now nullable.")
