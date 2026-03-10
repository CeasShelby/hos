from django import forms
from .models import Hostel

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


