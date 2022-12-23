from django.forms import ModelForm
from .models import Product


class CustomPostCreationForm(ModelForm):
    class Meta(object):
        model = Product
        fields = ["name", "description"]
