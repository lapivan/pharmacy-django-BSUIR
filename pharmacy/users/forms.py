from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone_number", "date_of_birth")
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'client'
        if commit:
            user.save()
        return user