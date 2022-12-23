from django.urls import path
from .models import Product
from .views import (
    ProductListView,
    create_product_order,
    edit_product_order,
    delete_product_order,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("create/", create_product_order, name="create-product-order"),
    path("edit/<str:pk>/", edit_product_order, name="edit-product-order"),
    path("delete/<str:pk>/", delete_product_order, name="delete-product-order"),
]
