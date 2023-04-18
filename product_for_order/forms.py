from django.forms import ModelForm
from .models import ProductForOrder


class CustomProductCreationForm(ModelForm):
    class Meta(object):
        model = ProductForOrder
        fields = ["name", "description"]


class CustomProductCreationManagerForm(ModelForm):
    class Meta(object):
        model = ProductForOrder
        fields = ["name", "description", "in_stock", "number_in_stock"]
