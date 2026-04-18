from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_age_profile_gender'),
    ]

    operations = [
        # These fields already exist in the DB, so we only include the new ones
        # and AlterField operations if needed. 
        # But for now, let's just add the missing study_spot.
        migrations.AddField(
            model_name='profile',
            name='study_spot',
            field=models.CharField(choices=[('hostel', 'Hostel'), ('library', 'Campus Library')], default='hostel', max_length=10),
        ),
        # Ensure weights are aligned in Django's state even if skip DB creation
        migrations.AlterField(
            model_name='profile',
            name='smoking_weight',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='study_weight',
            field=models.IntegerField(default=1),
        ),
    ]
