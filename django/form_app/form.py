from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password= forms.CharField(widget=forms.passwordInput(attrs={'class':'form_contro','placeholder':'password'}))
    password_confirmed = forms.CharField(widget=forms.passwordInput(attrs={'class':'form_control','placeholder':'confirm password'}))

    class Meta:
        model=User
        fields=['username','email']
        widgets={
            'username':forms.TextInput(attrs={'class':'form_control','placeholder':'username'}),
            'email':forms.emailInput(attrs={'class':'form_control','placeholder':'email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password=cleaned_data.get('password')
        password_confirmed = cleaned_data.get('password_confirmed')

        if password and password_confirmed and password != password_confirmed:
            raise forms.ValidationError('the password does not match')
        return cleaned_data
            
        