
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
            'phone', 'religion', 'region', 'hobbies', 
            'cleanliness', 'course', 'study_habit'
        ]
        
        # We use widgets to make it look good with Bootstrap
        widgets = {
            'phone': forms.TextInput(attrs={}),
            'religion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Christian, Muslim'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Central, Northern'}),
            'hobbies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What do you do for fun?'}),
            'cleanliness': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'study_habit': forms.Select(attrs={'class': 'form-select'}),
        }
    
