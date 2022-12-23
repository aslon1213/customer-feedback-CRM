# import forms from django
from django import forms
from .models import User


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["telephone_number", "address"]
