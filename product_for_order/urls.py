from django.urls import path
from .models import ProductForOrder
from .views import (
    ProductListView,
    create_product_order,
    edit_product_order,
    delete_product_order,
    auto_make_products,
    change_status,
    pdfmaker,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="order-list"),
    path("create/", create_product_order, name="create-product-order"),
    path("edit/<str:pk>/", edit_product_order, name="edit-product-order"),
    path("delete/<str:pk>/", delete_product_order, name="delete-product-order"),
    path("manager_change_status/", change_status, name="manager-change-status"),
    # for automation
    path("create_automation/", auto_make_products, name="create-automation"),
    path("topdf/", pdfmaker, name="order-to-pdf"),
]
