from models import Product
from django import forms
from django.forms import ModelForm
from .forms import CustomProductCreationForm


# make 100 products
for i in range(100):
    product = Product.objects.create(
        name=f"Product {i}",
        description=f"Product {i} description",
    )
    product.save()
