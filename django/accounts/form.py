
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    # Manually defining  fields to add Bootstrap classes
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), label="Confirm Password")
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name',]
        # Adding  Bootstrap classes to the automatic fields
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'first name'}),
            'last_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last name'}),
            'phone':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'phone number'})
        }

    # Validation for phone number (Strict 10 digits)
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit phone number (e.g., 0712345678).")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data


from .models import Profile # Don't forget to import your Profile model!

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # We list the fields we added to the Profile model earlier
        fields = [
            'gender', 'age', 'phone', 'religion', 'region', 'hobbies',
            'cleanliness', 'course', 'study_habit'
        ]
        
        # We use widgets to make it look good with Bootstrap
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your age', 'min': 16, 'max': 60}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Christian, Muslim'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Central, Northern'}),
            'hobbies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What do you do for fun?'}),
            'cleanliness': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'study_habit': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'gender': 'Gender',
            'age': 'Age',
        }
    

CHOICES = [(i, str(i)) for i in range(1, 6)] # 1 to 5 scale
class RoommatePreferenceForm(forms.ModelForm):
    CHOICES = [(i, str(i)) for i in range(1, 6)] # 1 to 5 scale

    class Meta:
        model = Profile
        fields = [
            'smoking_habit', 'smoking_weight', 
            'study_time', 'study_weight'
        ]
        widgets = {
            'smoking_habit': forms.Select(choices=CHOICES, attrs={'class': 'form-select bg-dark text-white'}),
            'smoking_weight': forms.Select(choices=CHOICES, attrs={'class': 'form-select bg-dark text-white'}),
            'study_time': forms.Select(choices=CHOICES, attrs={'class': 'form-select bg-dark text-white'}),
            'study_weight': forms.Select(choices=CHOICES, attrs={'class': 'form-select bg-dark text-white'}),
        }
        labels = {
            'smoking_habit': "Are you a smoker? (1: Never, 5: Heavy)",
            'smoking_weight': "How important is a roommate's smoking habit to you? (1: Don't care, 5: Deal-breaker)",
            'study_time': "When do you study? (1: Early Bird, 5: Night Owl)",
            'study_weight': "How important is sharing a study schedule? (1: Don't care, 5: Critical)",
        }


# Habit and Importance Scales with Descriptions
HABIT_SCALE = [
    (1, '1 (Never)'),
    (2, '2 (Rarely)'),
    (3, '3 (Occasionally)'),
    (4, '4 (Regularly)'),
    (5, '5 (Heavy)'),
]

DRINKING_SCALE = [
    (1, '1 (Never)'),
    (2, '2 (Rarely)'),
    (3, '3 (Occasionally)'),
    (4, '4 (Socially)'),
    (5, '5 (Regularly)'),
]

NOISE_SCALE = [
    (1, '1 (Silent/Library)'),
    (2, '2 (Quiet/Soft)'),
    (3, '3 (Moderate)'),
    (4, '4 (Lively/Music)'),
    (5, '5 (Loud/Extroverted)'),
]

VISITOR_SCALE = [
    (1, '1 (No visitors)'),
    (2, '2 (Rarely)'),
    (3, '3 (Occasionally)'),
    (4, '4 (Frequently)'),
    (5, '5 (Social Hub)'),
]

IMPORTANCE_SCALE = [
    (1, "1 (Don't care)"),
    (2, '2 (Minor)'),
    (3, '3 (Moderate)'),
    (4, '4 (Important)'),
    (5, '5 (Deal-breaker)'),
]

STUDY_TIME_CHOICES = [
    (1, '1 (Early Bird)'),
    (2, '2 (Morning)'),
    (3, '3 (Daytime)'),
    (4, '4 (Evening)'),
    (5, '5 (Night Owl)'),
]

class CombinedProfilePreferenceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'gender', 'age', 'phone', 'religion', 'region', 'hobbies',
            'course', 'is_early_bird',
            'cleanliness', 'cleanliness_weight',
            'smoking_habit', 'smoking_weight',
            'drinking_habit', 'drinking_weight',
            'religion_habit', 'religion_weight',
            'noise_habit', 'noise_weight',
            'study_time', 'study_weight',
            'study_spot', 'study_habit', 'visitors_habit',
        ]
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your age', 'min': 16, 'max': 60}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Christian, Muslim'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Central, Northern'}),
            'hobbies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'What do you do for fun?'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'is_early_bird': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'cleanliness': forms.Select(attrs={'class': 'form-select'}),
            'cleanliness_weight': forms.Select(choices=IMPORTANCE_SCALE, attrs={'class': 'form-select'}),
            
            'smoking_habit': forms.Select(choices=HABIT_SCALE, attrs={'class': 'form-select'}),
            'smoking_weight': forms.Select(choices=IMPORTANCE_SCALE, attrs={'class': 'form-select'}),
            
            'drinking_habit': forms.Select(choices=DRINKING_SCALE, attrs={'class': 'form-select'}),
            'drinking_weight': forms.Select(choices=IMPORTANCE_SCALE, attrs={'class': 'form-select'}),
            
            'religion_habit': forms.Select(attrs={'class': 'form-select'}),
            'religion_weight': forms.Select(choices=IMPORTANCE_SCALE, attrs={'class': 'form-select'}),
            
            'noise_habit': forms.Select(choices=NOISE_SCALE, attrs={'class': 'form-select'}),
            'noise_weight': forms.Select(choices=IMPORTANCE_SCALE, attrs={'class': 'form-select'}),
            
            'study_time': forms.Select(choices=STUDY_TIME_CHOICES, attrs={'class': 'form-select'}),
            'study_weight': forms.Select(choices=IMPORTANCE_SCALE, attrs={'class': 'form-select'}),
            
            'study_spot': forms.Select(attrs={'class': 'form-select'}),
            'study_habit': forms.Select(attrs={'class': 'form-select'}),
            'visitors_habit': forms.Select(choices=VISITOR_SCALE, attrs={'class': 'form-select'}),
        }
        labels = {
            'is_early_bird': "Are you an Early Bird?",
            'cleanliness': "Cleanliness Level",
            'cleanliness_weight': "Importance of cleanliness",
            'smoking_habit': "Do you smoke?",
            'smoking_weight': "Importance of a non-smoking roommate",
            'drinking_habit': "Do you drink?",
            'drinking_weight': "Importance of a non-drinking roommate",
            'religion_habit': "How do you practice your faith?",
            'religion_weight': "Importance of same religious style",
            'noise_habit': "Your noise level",
            'noise_weight': "Importance of similar noise tolerance",
            'study_time': "When do you study?",
            'study_weight': "Importance of shared study schedule",
            'study_spot': "Where do you prefer to study?",
            'study_habit': "How do you study?",
            'visitors_habit': "Frequency of visitors",
        }