from django import forms
from .models import Hostel, Booking

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = [
            'name', 'description', 'price_per_semester', 
            'distance_from_campus', 'gender_type', 
            'is_self_contained', 'main_photo',
            'is_quiet_environment', 'has_reading_room','room_phto', 'bath_photo', 'compound_photo'
        ]
        # Adding Bootstrap classes to make it look like EstateHub
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'})
            for field in ['name', 'price_per_semester', 'distance_from_campus']
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room_type', 'wants_roommate']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'form-select'}),
            'wants_roommate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'room_type': 'Room type',
            'wants_roommate': 'I want a roommate (double room only)',
        }

