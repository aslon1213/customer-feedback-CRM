# import forms from django
from django import forms
from .models import User


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
