from django.forms import ModelForm
from .models import Product


class CustomProductCreationForm(ModelForm):
    class Meta(object):
        model = Product
        fields = ["name", "description"]


class CustomProductCreationManagerForm(ModelForm):
    class Meta(object):
        model = Product
        fields = ["name", "description", "in_stock", "number_in_stock"]
