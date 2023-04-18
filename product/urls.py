from django.urls import path
from .views import *

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("create/", create_product, name="create-product"),
    path("edit/<str:pk>/", edit_product, name="edit-product"),
    path("delete/<str:pk>/", delete_product, name="delete-product"),
    path("create_auto/", auto_make_products, name="create-auto"),
    path("<str:pk>/", product_info, name="product-info"),
]
