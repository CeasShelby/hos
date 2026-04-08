from django.db import models
from django.contrib.auth.models import User

    # 1. THE HOSTEL CLASS (The Building)
class Hostel(models.Model):
    GENDER_CHOICES = [('M', 'Male Only'), ('F', 'Female Only'), ('X', 'Mixed')]
    
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    manager_phone = models.CharField(max_length=15, help_text="Contact for bookings")
    description = models.TextField()
    price_per_semester = models.DecimalField(max_digits=10, decimal_places=2)
    distance_from_campus = models.IntegerField(help_text="Distance in meters")
    gender_type = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_self_contained = models.BooleanField(default=True)
    total_rooms = models.IntegerField()
    available_rooms = models.IntegerField()
    main_photo = models.ImageField(upload_to='hostels/')

    
    # Feature: Student Interests Matching
    is_quiet_environment = models.BooleanField(default=True)
    has_reading_room = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    total_rooms = models.IntegerField(default=0) 
    available_rooms = models.IntegerField(default=0)
    room_phto = models.ImageField(upload_to='hostels/room_photos/', blank=True, null=True)
    bath_photo = models.ImageField(upload_to = 'hostels/bath_photos/', blank=True, null = True)
    compound_photo = models.ImageField(upload_to = 'hostels/compound_photos/', blank=True, null=True) 

# 2. THE BOOKING CLASS (The Action) - MUST BE OUTSIDE AND BELOW HOSTEL
class Booking(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE) # Now it can see 'Hostel'
    booked_at = models.DateTimeField(auto_now_add=True)
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
    ]
    status = models.CharField(max_length=20, default='Pending')
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='single')
    wants_roommate = models.BooleanField(
        default=False,
        help_text="Only relevant for double rooms",
    )

    def __str__(self):
        return f"{self.student.username} - {self.hostel.name}"

   
    
class RoommateProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_proposals')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_proposals')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver') # Prevents duplicate spam