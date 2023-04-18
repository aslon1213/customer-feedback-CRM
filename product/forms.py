from .models import Product
from django import forms

class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"