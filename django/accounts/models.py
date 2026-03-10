
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_early_bird = models.BooleanField(default=True)
    
    # New Roommate Matching Fields
    religion = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True, help_text="Home Region/District")
    hobbies = models.TextField(blank=True, help_text="List a few things you love")
    
    CLEAN_CHOICES = [
        ('neat', 'Very Neat/Organized'),
        ('average', 'Average'),
        ('relaxed', 'Relaxed/Messy'),
    ]
    cleanliness = models.CharField(max_length=10, choices=CLEAN_CHOICES, default='average')
    
    # Keep your old fields too
    course = models.CharField(max_length=100)
    study_habit = models.CharField(max_length=10, choices=[('quiet', 'Quiet'), ('group', 'Group')])

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
 