from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForms):
    password = forms.CharField(widget = forms.passwordInput)
    password_confirmed = forms.CharField(widget = forms.passwordInput, label='password confirm')

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'username']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmed = cleaned_data.get('password_confirmed')

        if password and password_confirmed and password != password_confirmed:
            raise forms.ValidationError('the password does not match') 